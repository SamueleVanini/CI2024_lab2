from abc import ABC, abstractmethod
from dataclasses import dataclass
import itertools
import numpy as np
from typing import Any, Callable, Collection

from tqdm import tqdm
from icecream import ic

SEED = 42


class BaseSolver(ABC):

    @property
    @abstractmethod
    def history(self) -> list:
        pass

    @property
    @abstractmethod
    def solution(self):
        pass

    @abstractmethod
    def solve():
        pass


class HillClimber(BaseSolver):

    def __init__(self, steps: int, tweak: Callable, fitness: Callable, init_sol) -> None:
        self.steps = steps
        self.tweak = tweak
        self.fitness = fitness
        self._solution = init_sol
        self._history = []
        self.solution_fitness = self.fitness(self._solution)

    @property
    def history(self) -> list:
        return self._history

    @property
    def solution(self):
        return self._solution

    def solve(self):
        for step in tqdm(range(self.steps)):
            new_sol = self.tweak(self._solution)
            f = self.fitness(new_sol)
            self._history.append(f)

            if f < self.solution_fitness:
                self._solution = new_sol
                self.solution_fitness = f


class HillClimberSimulatedAnnealing(HillClimber):

    BUFFER_SIZE = 5
    ONE_OUT_FIVE = BUFFER_SIZE / 5

    def __init__(
        self,
        steps: int,
        tweak: Callable[[Any, float], Any],
        fitness: Callable[..., Any],
        init_sol,
        strenght: float = 0.5,
    ) -> None:
        super().__init__(steps, tweak, fitness, init_sol)
        self.strenght = strenght
        self.buffer = []

    def solve(self):
        for step in tqdm(range(self.steps)):
            new_sol = self.tweak(self._solution, self.strenght)
            f = self.fitness(new_sol)
            self._history.append(f)

            self.buffer.append(f < self.solution_fitness)
            self.buffer = self.buffer[-self.BUFFER_SIZE :]

            if sum(self.buffer) > self.ONE_OUT_FIVE:
                self.strenght *= 1.3
            elif sum(self.buffer) < self.ONE_OUT_FIVE:
                self.strenght /= 1.0001

            if f < self.solution_fitness:
                self._solution = new_sol
                self.solution_fitness = f


@dataclass
class Individual:
    genome: list[int]
    fitness: float = None


class EAStadyState(BaseSolver):

    def __init__(
        self,
        generations: int,
        tweak: Callable[[Any, float], Any],
        fitness: Callable[..., Any],
        init_genome=None,
        population: int | list[Individual] = 30,
        offspring: int = 20,
        rnd: np.random.Generator = None,
    ) -> None:
        self.generations = generations
        self.tweak = tweak
        self.fitness = fitness
        self._history = []
        if isinstance(population, int):
            self._pop_size = population
            self._population = [
                Individual(genome, fitness(genome)) for genome in itertools.repeat(init_genome, population)
            ]
        if isinstance(population, list):
            self._pop_size = len(population)
            self._population = population
        self.n_offspring = offspring
        if rnd is None:
            self.rnd = np.random.default_rng(SEED)
        else:
            self.rnd = rnd

    @property
    def history(self) -> list:
        return self._history

    @property
    def solution(self):
        return self._population[0].genome

    @property
    def solution_fitness(self):
        return self._population[0].fitness

    def solve(self):
        for generation in tqdm(range(self.generations)):
            parrents = self.rnd.choice(self._population, size=self.n_offspring, replace=False)
            offsprings = []
            for parrent in parrents:
                genome = self.tweak(parrent.genome)
                fit = self.fitness(genome)
                self._history.append(fit)
                offsprings.append(Individual(genome, fit))
            self._population.extend(offsprings)
            self._population.sort(key=lambda i: i.fitness)
            self._population = self._population[: self._pop_size]
