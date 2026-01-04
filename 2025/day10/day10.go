// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"log"
	"log/slog"
)

//const fileName string = "day10-test.txt"

const fileName string = "day10-input.txt"

func main() {
	slog.SetLogLoggerLevel(slog.LevelDebug)

	// Slurp file
	machines := ReadFile(fileName)

	// part1 := 0
	// for _, m := range machines {
	// 	part1 += SelectButtons_part1(&m)
	// }
	// log.Printf("Part 1: %v\n", part1)

	ch := make(chan int, len(machines))
	for i := range machines {
		go SelectButtons_part2(&machines[i], ch)
	}
	part2 := 0
	for range machines {
		part2 += <-ch
	}
	log.Printf("Part 2: %v\n", part2)
}
