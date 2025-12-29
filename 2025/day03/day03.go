// Advent of Code 2025 | https://adventofcode.com/2025/day/2
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"bufio"
	"log"
	"os"
)

const FileName string = "day03-test.txt"

// const FileName string = "day03-input.txt"

type Bank string

func ReadFile(fileName string) []Bank {
	file, err := os.Open(FileName)
	if err != nil {
		log.Panicf("Yeuch: %v", err)
	}
	defer file.Close()

	var banks []Bank
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		banks = append(banks, Bank(scanner.Text()))
	}
	return banks
}

func main() {
	banks := ReadFile(FileName)
	log.Print(banks)

	// = [Part 1] =================================================================================

	// = [Part 2] =================================================================================

}
