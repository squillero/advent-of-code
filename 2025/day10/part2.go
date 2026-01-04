// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"log"
	"slices"
	"sync/atomic"
)

type buttonRange struct {
	from int
	to   int
}

type Solution struct {
	machine      *Machine
	buttons      []int
	buttonRanges []buttonRange
	numPresses   int
	numButtons   int
	numJoltages  int
	tmpWired     [][]bool
	tmpCount     []int
}

// var buttonRanges []buttonRange

func defineFromTo(sol *Solution) (int, int) {
	var b int
	for b = 0; b < len(sol.buttons); b++ {
		sol.buttonRanges[b].from = sol.buttons[b]
		sol.buttonRanges[b].to = sol.buttons[b] + 1
	}
	for ; b < sol.numButtons; b++ {
		sol.buttonRanges[b].from = 0
		sol.buttonRanges[b].to = 1 << 30 // a big number
	}

	// Update target Joltages
	target := slices.Clone(sol.machine.JoltageRequirements)
	for button, num := range sol.buttons {
		for _, wiring := range sol.machine.ButtonWirings[button] {
			if target[wiring] -= num; target[wiring] < 0 {
				return -1, -1
			}
		}
	}

	// Find which button affect which joltage
	for _, w := range sol.tmpWired {
		for i := range w {
			w[i] = false // reset
		}
	}
	for b := len(sol.buttons); b < sol.numButtons; b++ {
		for _, joltage := range sol.machine.ButtonWirings[b] {
			sol.tmpWired[b][joltage] = true
		}
	}

	// Count button wirings for each Joltage
	for i := range sol.tmpCount {
		sol.tmpCount[i] = 0 // clear
	}
	for w := len(sol.buttons); w < len(sol.machine.ButtonWirings); w++ {
		for _, j := range sol.machine.ButtonWirings[w] {
			sol.tmpCount[j] += 1
		}
	}

	// Set .from and .to
	for button := range sol.tmpWired {
		for joltage, wired := range sol.tmpWired[button] {
			if wired && sol.tmpCount[joltage] == 0 {
				log.Fatalln("Zero!")
			} else if wired && sol.tmpCount[joltage] == 1 {
				sol.buttonRanges[button].from = target[joltage]
				sol.buttonRanges[button].to = target[joltage] + 1
			} else if wired && sol.buttonRanges[button].to > target[joltage]+1 {
				sol.buttonRanges[button].to = target[joltage] + 1
			}
		}
	}
	return sol.buttonRanges[len(sol.buttons)].from, sol.buttonRanges[len(sol.buttons)].to
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

var TaskStartedCounter, TaskCompletedCounter int32

func SelectButtons_part2(machine *Machine, ch chan<- int) {
	currentSolution := Solution{
		machine:      machine,
		buttons:      make([]int, 0, len(machine.ButtonWirings)),
		buttonRanges: make([]buttonRange, len(machine.ButtonWirings)),
		numPresses:   0,
		numButtons:   len(machine.ButtonWirings),
		numJoltages:  len(machine.JoltageRequirements),
		tmpWired:     make([][]bool, len(machine.ButtonWirings)),
		tmpCount:     make([]int, len(machine.JoltageRequirements)),
	}
	for b := range currentSolution.tmpWired {
		currentSolution.tmpWired[b] = make([]bool, currentSolution.numJoltages)
	}

	bestSolution := Solution{
		machine:      machine,
		buttons:      nil,
		buttonRanges: nil,
		numPresses:   1 << 30, // a large number (int is "at least" 32 bit)
		numButtons:   currentSolution.numButtons,
		numJoltages:  currentSolution.numJoltages,
		tmpWired:     nil,
		tmpCount:     nil,
	}

	atomic.AddInt32(&TaskStartedCounter, 1)
	thisTask := TaskStartedCounter
	recursiveSelectButtons_part2(0, &currentSolution, &bestSolution)
	atomic.AddInt32(&TaskCompletedCounter, 1)
	log.Printf("Task %d (%.2f%% completed): Found a solution with %d presses %v\n",
		thisTask, 100*float32(TaskCompletedCounter)/float32(TaskStartedCounter), bestSolution.buttons, bestSolution.numPresses)
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
	from, to := defineFromTo(current)
	for p := from; p < to; p++ {
		current.buttons = append(current.buttons, p)
		current.numPresses += p
		recursiveSelectButtons_part2(index+1, current, best)
		current.numPresses -= p
		current.buttons = current.buttons[:len(current.buttons)-1]
	}
	return false
}
