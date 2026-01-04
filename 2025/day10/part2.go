// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"log"
	"slices"
)

type buttonRange struct {
	from int
	to   int
}

type Solution struct {
	machine     *Machine
	buttons     []int
	numPresses  int
	numButtons  int
	numJoltages int
}

// var buttonRanges []buttonRange

func updateMinMax(sol *Solution) []buttonRange {
	// Output: Valid ranges for buttons' presses
	ranges := make([]buttonRange, sol.numButtons)
	var b int
	for b = 0; b < len(sol.buttons); b++ {
		ranges[b].from = sol.buttons[b]
		ranges[b].to = sol.buttons[b] + 1
	}
	for ; b < sol.numButtons; b++ {
		ranges[b].from = 0
		ranges[b].to = 1000000
	}

	// Update target Joltages
	target := slices.Clone(sol.machine.JoltageRequirements)
	for button, num := range sol.buttons {
		for _, wiring := range sol.machine.ButtonWirings[button] {
			if target[wiring] -= num; target[wiring] < 0 {
				return nil
			}
		}
	}

	// Find which button affect which joltage
	wired := make([][]bool, sol.numButtons)
	for b := range wired {
		wired[b] = make([]bool, sol.numJoltages)
	}
	for b := len(sol.buttons); b < sol.numButtons; b++ {
		for _, joltage := range sol.machine.ButtonWirings[b] {
			wired[b][joltage] = true
		}
	}

	// Count button wirings for each Joltage
	count := make([]int, len(target))
	for w := len(sol.buttons); w < len(sol.machine.ButtonWirings); w++ {
		for _, j := range sol.machine.ButtonWirings[w] {
			count[j] += 1
		}
	}

	// Set .from and .to
	for button := range wired {
		for joltage, wired := range wired[button] {
			if wired && count[joltage] == 0 {
				log.Fatalln("Zero!")
			} else if wired && count[joltage] == 1 {
				ranges[button].from = target[joltage]
				ranges[button].to = target[joltage] + 1
			} else if wired && ranges[button].to > target[joltage]+1 {
				ranges[button].to = target[joltage] + 1
			}
		}
	}
	return ranges
}

// var bestSolution, currentSolution Solution

func valid(sol *Solution) bool {
	current := slices.Clone(sol.machine.JoltageRequirements)
	for b, pushes := range sol.buttons {
		for _, wiring := range sol.machine.ButtonWirings[b] {
			current[wiring] -= pushes
		}
	}
	for i := range current {
		if current[i] != 0 {
			return false
		}
	}
	return true
}

func SelectButtons_part2(machine *Machine, ch chan int) {
	currentSolution := Solution{
		machine:     machine,
		buttons:     make([]int, 0, len(machine.ButtonWirings)),
		numPresses:  0,
		numButtons:  len(machine.ButtonWirings),
		numJoltages: len(machine.JoltageRequirements),
	}
	bestSolution := Solution{
		machine:     machine,
		buttons:     nil,
		numPresses:  1 << 30, // a large number (int is "at least" 32 bit)
		numButtons:  currentSolution.numButtons,
		numJoltages: currentSolution.numJoltages,
	}

	recursiveSelectButtons_part2(0, &currentSolution, &bestSolution)
	log.Printf("Found a solution: %v (%v presses)\n", bestSolution.buttons, bestSolution.numPresses)
	ch <- bestSolution.numPresses
}

func recursiveSelectButtons_part2(index int, current *Solution, best *Solution) bool {
	if current.numPresses >= best.numPresses {
		return true
	}
	if index == current.numButtons {
		if valid(current) && current.numPresses < best.numPresses {
			// log.Printf("Complete solution: %v (%v)\n", current.buttons, valid(&current))
			best.buttons = slices.Clone(current.buttons)
			best.numPresses = current.numPresses
		}
		return true
	}
	if possiblePresses := updateMinMax(current); possiblePresses != nil {
		for p := possiblePresses[index].from; p < possiblePresses[index].to; p++ {
			current.buttons = append(current.buttons, p)
			current.numPresses += p
			recursiveSelectButtons_part2(index+1, current, best)
			current.numPresses -= p
			current.buttons = current.buttons[:len(current.buttons)-1]
		}
	} else {
		// Already overflowed
		return true
	}
	return false
}
