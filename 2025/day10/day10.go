// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"log"

	"github.com/squillero/advent-of-code/2025/go/day10/algorithm"
	"github.com/squillero/advent-of-code/2025/go/day10/data"
)

//const fileName string = "day10-test.txt"

const fileName string = "day10-input.txt"

func main() {
	// Slurp file
	machines := data.ReadFile(fileName)

	part1 := 0
	for _, m := range machines {
		part1 += algorithm.SelectButtons_part1(&m)
	}
	log.Printf("Part 1: %v\n", part1)

	part2 := 0
	for _, m := range machines {
		part2 += algorithm.SelectButtons_part2(&m)
	}
	log.Printf("Part 2: %v\n", part2)
}
