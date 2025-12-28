// Advent of Code 2025 | https://adventofcode.com/2025/day/2
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

const FileName string = "day02-test.txt"

// const FileName string = "day02-input.txt"

type Range struct {
	From uint
	To   uint
}

func main() {
	// Slurp file
	ranges := ReadFile(FileName)

	// Part 1
	// Note: GoLang RE2 engine *DOES NOT* support backrefs like "^(.+)\1$"
	for i, r := range ranges {
		log.Println("%v: %v-%v", i, r.From, r.To)
	}

}

func ReadFile(fileName string) []Range {
	file, err := os.Open(FileName)
	if err != nil {
		log.Panicf("Yeuch: %v", err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	scanner.Scan() // slurp first (only) line
	line := scanner.Text()

	var ranges []Range
	for _, block := range strings.Split(line, ",") {
		tok := strings.Split(block, "-")
		from, _ := strconv.Atoi(tok[0]) // can't fail ;-)
		to, _ := strconv.Atoi(tok[1])   // can't fail ;-)
		ranges = append(ranges, Range{
			From: uint(from),
			To:   uint(to),
		})
	}

	return ranges
}
