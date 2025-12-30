// Advent of Code 2025 | https://adventofcode.com/2025/day/3
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"bufio"
	"log"
	"os"
)

//const FileName string = "day03-test.txt"

const FileName string = "day03-input.txt"

type Bank []int

func (B Bank) maxIndex(from, to int) int {
	m := from
	for i := from + 1; i < to; i++ {
		if B[i] > B[m] {
			m = i
		}
	}
	return m
}

func readFile(fileName string) []Bank {
	file, err := os.Open(FileName)
	if err != nil {
		log.Panicf("Yeuch: %v", err)
	}
	defer file.Close()

	var banks []Bank
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		var b Bank
		for _, c := range scanner.Text() {
			b = append(b, int(c-'0'))
		}
		banks = append(banks, b)
	}
	return banks
}

func calculateChecksum(batteryBanks []Bank, numBatteries int) uint64 {
	var checksum uint64 = 0
	for _, bank := range batteryBanks {
		var joltage uint64 = 0
		i := -1
		for b := numBatteries - 1; b >= 0; b-- {
			i = bank.maxIndex(i+1, len(bank)-b)
			joltage = joltage*10 + uint64(bank[i])
		}
		checksum += joltage
	}
	return checksum
}

func main() {
	banks := readFile(FileName)

	// = [Part 1] =================================================================================
	log.Printf("Checksum (part 1): %v\n", calculateChecksum(banks, 2))

	// = [Part 2] =================================================================================
	log.Printf("Checksum (part 2): %v\n", calculateChecksum(banks, 12))

}
