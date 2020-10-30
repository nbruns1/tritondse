import array
import glob
import logging
import os
import time

from array                      import array
from hashlib                    import md5
from tritondse.enums            import CoverageStrategy
from tritondse.config           import Config
from tritondse.seed             import Seed, SeedFile
from tritondse.callbacks        import CallbackManager
from tritondse.coverage         import Coverage
from tritondse.path_constraints import PathConstraintsHash
from tritondse.worklist         import *
from tritondse.types            import *



class SeedsManager:
    """
    This class is used to represent the seeds management.
    """
    def __init__(self, config: Config, callbacks: CallbackManager):
        self.config           = config
        self.coverage         = Coverage()
        self.path_constraints = PathConstraintsHash()
        self.worklist         = WorklistAddressToSet(config, self.coverage) # TODO: Use the appropriate worklist according to config and the strategy wanted
        self.cbm              = callbacks
        self.corpus           = set()
        self.crash            = set()

        self.__init_dirs()


    def __load_seed_from_file(self, path):
        logging.debug('Loading %s' % (path))
        return SeedFile(path)


    def __init_dirs(self):
        # --------- Initialize METADATA --------------------------------------
        if not os.path.isdir(self.config.metadata_dir):
            logging.debug('Creating the %s directory' % (self.config.metadata_dir))
            os.mkdir(self.config.metadata_dir)
        else:
            logging.debug('Loading the existing metadata directory from %s' % (self.config.metadata_dir))
            # Loading coverage
            self.coverage.load_from_disk(self.config.metadata_dir)
            # Loading path constraints
            self.path_constraints.load_from_disk(self.config.metadata_dir)


        # --------- Initialize WORKLIST --------------------------------------
        if not os.path.isdir(self.config.worklist_dir):
            logging.debug('Creating the %s directory' % (self.config.worklist_dir))
            os.mkdir(self.config.worklist_dir)
        else:
            logging.debug('Checking the existing worklist directory from %s' % (self.config.worklist_dir))
            for path in glob.glob('%s/*.cov' % (self.config.worklist_dir)):
                self.worklist.add(self.__load_seed_from_file(path))


        # --------- Initialize CORPUS ----------------------------------------
        if not os.path.isdir(self.config.corpus_dir):
            logging.debug('Creating the %s directory' % (self.config.corpus_dir))
            os.mkdir(self.config.corpus_dir)
        else:
            logging.debug('Checking the existing corpus directory from %s' % (self.config.corpus_dir))
            for path in glob.glob('%s/*.cov' % (self.config.corpus_dir)):
                self.corpus.add(self.__load_seed_from_file(path))


        # --------- Initialize CRASH -----------------------------------------
        if not os.path.isdir(self.config.crash_dir):
            logging.debug('Creating the %s directory' % (self.config.crash_dir))
            os.mkdir(self.config.crash_dir)
        else:
            logging.debug('Checking the existing crash directory from %s' % (self.config.crash_dir))
            for path in glob.glob('%s/*.cov' % (self.config.crash_dir)):
                self.crash.add(self.__load_seed_from_file(path))


    def __save_metadata_on_disk(self):
        # Save coverage
        self.coverage.save_on_disk(self.config.metadata_dir)
        # Save path constraints
        self.path_constraints.save_on_disk(self.config.metadata_dir)


    def __try_lighter_model(self, ctx, end_pc, only_one=False):
        constraint = self.__get_thread_pc(ctx, end_pc)
        astCtxt = ctx.getAstContext()
        constraint.append(astCtxt.lnot(end_pc.getTakenPredicate()))
        status = SOLVER.TIMEOUT
        index = 0

        while status == SOLVER.TIMEOUT:
            ts = time.time()
            if only_one:
                # Solve the current constraint without any predicate
                model, status = ctx.getModel(constraint[-1], status=True)
                te = time.time()
                logging.info(f'Sending lighter query to the solver (size: 1). Solving time: {te - ts} seconds. Status: {status}')
            elif len(constraint[index:]) >= 2:
                model, status = ctx.getModel(astCtxt.land(constraint[index:]), status=True)
                te = time.time()
                logging.info(f'Sending lighter query to the solver (size: {len(constraint[index:])}). Solving time: {te - ts} seconds. Status: {status}')
            else:
                return {}
            index += 100 % len(constraint)

        return model


    def __get_thread_pc(self, ctx, end_pc):
        thread_id = end_pc.getThreadId()
        astCtxt = ctx.getAstContext()
        constraints = [astCtxt.equal(astCtxt.bvtrue(), astCtxt.bvtrue())]
        pco = ctx.getPathConstraints()
        for pc in pco:
            #if pc.getThreadId() != thread_id:
            #    continue
            if pc.getBranchConstraints() == end_pc.getBranchConstraints():
                return constraints
            constraints.append(pc.getTakenPredicate())


    def __get_new_inputs(self, execution):
        # Set of new inputs
        inputs = set()

        # Get path constraints from the last execution
        pco = execution.pstate.tt_ctx.getPathConstraints()

        # Get the astContext
        astCtxt = execution.pstate.tt_ctx.getAstContext()

        # We start with any input. T (Top)
        previousConstraints = [
            astCtxt.equal(astCtxt.bvtrue(), astCtxt.bvtrue()),
            astCtxt.equal(astCtxt.bvtrue(), astCtxt.bvtrue())
        ]

        # Define a limit of branch constraints
        smt_queries = 0

        # The hash representation of a taken path and constraints asked
        pc_hash_repr = md5()

        # Go through the path constraints
        for pc in pco:

            # Update the hash representation of the taken path
            if self.config.coverage_strategy == CoverageStrategy.PATH_COVERAGE:
                pc_hash_repr.update(array('L', [pc.getTakenAddress()]))

            elif self.config.coverage_strategy == CoverageStrategy.CODE_COVERAGE:
                pc_hash_repr = md5(array('L', [pc.getTakenAddress()]))

            # Save the constraint
            self.path_constraints.add_hash_constraint(pc_hash_repr.hexdigest())

            # If there is a condition
            if pc.isMultipleBranches():

                # Get all branches
                branches = pc.getBranchConstraints()
                for branch in branches:

                    if branch['isTaken'] and self.config.coverage_strategy == CoverageStrategy.EDGE_COVERAGE:
                        h = md5(array('L', [branch['srcAddr'], branch['dstAddr']]))
                        self.path_constraints.add_hash_constraint(h.hexdigest())

                    # Get the constraint of the branch which has not been taken.
                    if not branch['isTaken']:

                        if self.config.coverage_strategy == CoverageStrategy.PATH_COVERAGE:
                            # In path coverage, we have to fork the hash of the current
                            # pc for each branch we want to revert
                            forked_hash = pc_hash_repr.copy()
                            forked_hash.update(array('L', [branch['dstAddr']]))

                        elif self.config.coverage_strategy == CoverageStrategy.CODE_COVERAGE:
                            forked_hash = md5(array('L', [branch['dstAddr']]))

                        elif self.config.coverage_strategy == CoverageStrategy.EDGE_COVERAGE:
                            forked_hash = md5(array('L', [branch['srcAddr'], branch['dstAddr']]))

                        # Create the constraint
                        constraint = astCtxt.land(previousConstraints + [branch['constraint']])

                        # Only ask for a model if the constraints has never been asked
                        if self.path_constraints.hash_already_asked(forked_hash.hexdigest()) is False:
                            ts = time.time()
                            model, status = execution.pstate.tt_ctx.getModel(constraint, status=True)
                            te = time.time()
                            smt_queries += 1
                            logging.info(f'Sending query n°{smt_queries} to the solver. Solving time: {te - ts:.02f} seconds. Status: {status}')

                            # Save the hash of the constraint
                            self.path_constraints.add_hash_constraint(forked_hash.hexdigest())

                            models = list([model])
                            if status == Solver.TIMEOUT:
                                models.append(self.__try_lighter_model(execution.pstate.tt_ctx, pc))
                                models.append(self.__try_lighter_model(execution.pstate.tt_ctx, pc, only_one=True))

                            for model in models:
                                # Current content before getting model
                                content = bytearray(execution.seed.content)
                                # For each byte of the seed, we assign the value provided by the solver.
                                # If the solver provide no model for some bytes of the seed, their value
                                # stay unmodified (with their current value).
                                for k, v in sorted(model.items()):
                                    content[k] = v.getValue()

                                # Calling callback if user defined one
                                for cb in self.cbm.get_new_input_callback():
                                    cont = cb(execution, execution.pstate, content)
                                    # if the callback return a new input continue with that one
                                    content = cont if cont is not None else content

                                # Create the Seed object and assign the new model
                                seed = Seed(bytes(content))
                                # Note: branch[] contains information that can help the SeedManager to classify its
                                # seeds insertion:
                                #
                                #   - branch['srcAddr'] -> The location of the branch instruction
                                #   - branch['dstAddr'] -> The destination of the jump if and only if branch['isTaken'] is True.
                                #                          Otherwise, the destination address is the next linear instruction.
                                seed.target_addr = branch['dstAddr']
                                # Add the seed to the set of new inputs
                                inputs.add(seed)

            # Update the previous constraints with true branch to keep a good path.
            previousConstraints.append(pc.getTakenPredicate())

            # Check if we reached the limit of query
            if self.config.smt_queries_limit and smt_queries >= self.config.smt_queries_limit:
                break

        return inputs


    def pick_seed(self):
        return self.worklist.pick()


    def add_seed(self, seed):
        if seed and seed not in self.corpus and seed not in self.crash:
            seed.save_on_disk(self.config.worklist_dir)
            self.worklist.add(seed)
            logging.info(f'Seed dumped into {self.config.worklist_dir}/{seed.get_file_name()}')


    def post_execution(self, execution, seed):
        # Update instructions covered from the last execution into our exploration coverage
        self.coverage.merge(execution.coverage)

        # Add the seed to the current corpus
        self.corpus.add(seed)

        # Generate new inputs
        logging.info('Getting models, please wait...')
        inputs = self.__get_new_inputs(execution)
        for m in inputs:
            # Check if we already have executed this new seed
            if m and m not in self.corpus and m not in self.crash:
                self.worklist.add(m)
                m.save_on_disk(self.config.worklist_dir)
                logging.info(f'Seed dumped into {self.config.worklist_dir}/{m.get_file_name()}')

        # Save the current seed into the corpus directory  and remove it from
        # the worklist directory.
        seed.save_on_disk(self.config.corpus_dir)
        seed.remove_from_disk(self.config.worklist_dir)
        logging.info(f'Corpus dumped into {self.config.corpus_dir}/{seed.get_file_name()}')

        # Save metadata on disk
        self.__save_metadata_on_disk()

        logging.info('Worklist size: %d' % (len(self.worklist)))
        logging.info('Corpus size: %d' % (len(self.corpus)))
        logging.info('Total of instructions covered: %d' % (self.coverage.number_of_instructions_covered()))
