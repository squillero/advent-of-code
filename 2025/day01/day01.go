// Advent of Code 2025 | https://adventofcode.com/2025/day/1
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
)

const fileName string = "day01-test.txt"

// const fileName string = "day01-input.txt"

func main() {
	// Slurp file
	turns := readFile(fileName)

	// Part 1
	dial := 50
	password := 0
	for _, ticks := range turns {
		dial += ticks
		if dial%100 == 0 {
			password += 1
		}
	}
	log.Printf("Password (part 1): %v\n", password)

	// Part 2
	dial = 50
	password = 0
	for _, tickCounter := range turns {
		var tick, count int
		if tickCounter > 0 {
			tick = 1
			count = tickCounter
		} else {
			tick = -1
			count = -tickCounter
		}
		for t := 0; t < count; t++ {
			dial += tick
			if dial%100 == 0 {
				password += 1
			}
		}
	}
	log.Printf("Password (part 2): %v\n", password)
}

func readFile(fileName string) []int {
	file, err := os.Open(fileName)
	if err != nil {
		log.Panicf("%v", err)
	}
	defer file.Close()

	var movements []int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		t, _ := strconv.Atoi(line[1:])
		if rune(line[0]) == 'R' {
			movements = append(movements, t)
		} else {
			movements = append(movements, -t)
		}
	}
	return movements
}
