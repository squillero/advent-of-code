// Advent of Code 2025 | https://adventofcode.com/2025/day/1
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	// "log/slog"
	"bufio"
	"log"
	"os"
	"strconv"
)

const FileName string = "day01-test.txt"

func main() {
	// Slurp file
	turns := ReadFile(FileName)

	// Part 1
	password := 0
	dial := 50
	for _, turn := range turns {
		dial += turn
		if dial%100 == 0 {
			password += 1
		}
	}
	log.Printf("Password (part 1): %v\n", password)

	// Part 2
	password = 0
	dial = 50
	for _, turn := range turns {
		var tick, count int
		if turn > 0 {
			tick = 1
			count = turn
		} else {
			tick = -1
			count = -turn
		}
		for t := 0; t < count; t += 1 {
			dial += tick
			if dial%100 == 0 {
				password += 1
			}
		}
	}
	log.Printf("Password (part 2): %v\n", password)
}

func ReadFile(fileName string) []int {
	file, err := os.Open(FileName)
	if err != nil {
		log.Panicf("%v", err)
	}
	defer file.Close()

	var movements []int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		t, _ := strconv.Atoi(line[1:])
		if rune(line[0]) == 'L' {
			t = -t
		}
		movements = append(movements, t)
	}
	return movements
}
