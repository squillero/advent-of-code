// Advent of Code 2025 | https://adventofcode.com/2025/day/2
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
)

//const FileName string = "day02-test.txt"

const FileName string = "day02-input.txt"

type Range struct {
	From uint64
	To   uint64
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
			From: uint64(from),
			To:   uint64(to),
		})
	}

	return ranges
}

func checkValidity(rng Range) uint64 {
	var checksum uint64 = 0

	for t := rng.From; t <= rng.To; t += 1 {
		id := fmt.Sprintf("%d", t)
		if len(id)%2 == 0 && id[:len(id)/2] == id[len(id)/2:] {
			// log.Printf("Illegal id \"%v\": \"%d\" == \"%d\"", id, id[:len(id)/2], id[len(id)/2:])
			checksum += t
		}
	}
	return checksum
}

func checkValidityEnhanced(rng Range) uint64 {
	var checksum uint64 = 0

	for t := rng.From; t <= rng.To; t += 1 {
		id := fmt.Sprintf("%d", t)
		valid := true
		for l := 1; l < len(id) && valid; l += 1 {
			if len(id)%l > 0 {
				continue
			}
			tmp := false
			for t := 0; t*l < len(id); t += 1 {
				if id[:l] != id[t*l:(t+1)*l] {
					// log.Printf("Mismatch: id=%v, t=%v, l=%v\n", id, t, l)
					tmp = true
					break
				}
			}
			if !tmp {
				// log.Printf("Illegal: id=%v (patter of len %v)\n", id, l)
				valid = false
			}
		}
		if !valid {
			// log.Printf("Illegal id \"%v\"\n", id)
			checksum += t
		}
	}
	return checksum
}

func main() {
	ranges := ReadFile(FileName)

	var wg sync.WaitGroup
	var checksum uint64
	// = [Part 1] =================================================================================
	// This is Go, let's do it in parallel!
	// Note: The RE2 engine does not support backref as in "^(.+)\1$"
	checksum = 0
	for _, rng := range ranges {
		wg.Add(1)
		go func(r Range) {
			defer wg.Done()
			v := checkValidity(r)          // rng would be safe in Go1.22+
			atomic.AddUint64(&checksum, v) // avoid races
		}(rng) // loop variable capture (ie. no closure on loop variable!)
	}
	wg.Wait() // wait for all go routines to complete
	log.Printf("Puzzle answer (part 1): %d\n", checksum)

	// = [Part 2] =================================================================================
	checksum = 0
	for _, rng := range ranges {
		wg.Add(1)
		go func(r Range) {
			defer wg.Done()
			v := checkValidityEnhanced(r)
			atomic.AddUint64(&checksum, v)
		}(rng)
	}
	wg.Wait()
	log.Printf("Puzzle answer (part 2): %d\n", checksum)
}
