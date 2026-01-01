// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package algorithm

import (
	"log"

	"github.com/squillero/advent-of-code/2025/go/day10/data"
)

// Checks whether the pressed buttons meet the machine's joltage requirements.
//
//	> 0 : joltage level exceeds the requirement in at least one counter
//	< 0 : joltage level is below requirement in a counter and never above
//	= 0 : joltage level is correct
func compareJoltage() int {
	target := currentMachine.JoltageRequirements
	current := make([]int, len(currentMachine.JoltageRequirements))
	for i, m := range selectedButtons {
		for _, w := range currentMachine.ButtonWirings[i] {
			current[w] += m
		}
	}

	returnValue := 0
	for i := range current {
		if current[i] > target[i] {
			return 1
		} else if current[i] < target[i] {
			returnValue = -1
		}
	}
	return returnValue
}

func sum(v []int) int {
	s := 0
	for _, v := range v {
		s += v
	}
	return s
}

func SelectButtons_part2(m *data.Machine) int {
	currentMachine = m // stop passing around the machine
	selectedButtons = make([]int, len(m.ButtonWirings))
	bestSolutionButtons = 99999999
	log.Printf("Finding Joltage for machine %v\n", m)
	recursiveSelection(0)
	return bestSolutionButtons
}

func recursiveSelection(i int) bool {
	eval := compareJoltage()
	//log.Printf("%v -> %v\n", selectedButtons, eval)
	//log.Printf("Buttons: %v -- eval: %v\n", selectedButtons, eval)

	if sum(selectedButtons) >= bestSolutionButtons {
		//log.Printf("Giving up: already found a solution with %v buttons\n", bestSolutionButtons)
		return false
	}

	if eval == 0 {
		bestSolutionButtons = sum(selectedButtons)
		log.Printf("Eureka: found a solution with %v buttons -- %v\n", bestSolutionButtons, selectedButtons)
	} else if eval > 0 {
		// log.Println("No need to continue")
		// log.Printf("Giving up: overflowed\n")
		return false
	}
	if i == len(selectedButtons) {
		return true
	}

	//selectedButtons[i]++
	//log.Printf("selectedButtons[%v] = %v\n", i, selectedButtons[i])
	for recursiveSelection(i + 1) {
		selectedButtons[i]++
		//log.Printf("selectedButtons[%v] = %v\n", i, selectedButtons[i])
	}
	selectedButtons[i] = 0
	return true
}
