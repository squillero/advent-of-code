// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package main

import (
	"log"
)

// Select the minimum number of buttons to match LightDiagram
func SelectButtons_part1(machine *Machine) int {
	numButtons := len(machine.ButtonWirings)
	var selected []int

	// Checks wether pressing the selected buttons match machine's Light Diagram
	target := machine.LightDiagram
	current := make([]bool, len(machine.LightDiagram))
	valid := func(buttons []int) bool {
		for i := range current {
			current[i] = false // reset `current`
		}
		for i := 0; i < len(buttons)-1; i++ {
			for _, w := range machine.ButtonWirings[buttons[i]] {
				current[w] = !current[w]
			}
		}
		for i := range current {
			if current[i] != target[i] {
				return false
			}
		}
		return true
	}

	for numSelected := 1; numSelected <= numButtons; numSelected++ {
		// look for a solution using exactly `numSelected` buttons out of numButtons
		// order does not matter, and selecting a button twice resets the wirings
		selected = make([]int, numSelected+1)
		for i := 0; i <= numSelected; i++ {
			selected[i] = numSelected - i - 1 // the (n+1)-th button in -1
		}

		for selected[numSelected] < 0 { // loop while (n+1)-th button is -1
			if valid(selected) {
				return numSelected
			}

			// selected: the buttons we want to press
			// rule: selected[i] > selected[j] if i < j -- it's a combination
			// Example: numButtons is 5; numSelected is 3
			//// selected = [4 3 0 -1] -> Press buttons: 4, 3, and 0
			//// find the next selection:
			//// 4 can't be increased (buttons are {0, 1, 2, 3, 4})
			//// 3 can't be increased (button[1] must be < button[0])
			//// first possibility: button[2] -> change 0 to 1
			//// then button[1] is set to 2 ie. button[2] + 1
			//// then button[0] is set to 3 ie. button[1] + 1
			//// select = [3 2 1 -1] -> Press buttons: 3, 2, and 1
			//// next will be: select = [4 2 1 -1]
			//// next will be: select = [4 3 1 -1]
			//// next will be: select = [4 3 2 -1]
			//// then, finally: select = [3 2 1 0] (and that's the end!)
			if selected[0] < numButtons-1 {
				// change first button. eg. [3 1 0 -1] => [4 1 0 -1]
				selected[0]++
			} else {
				// can't pick 'next one' for the first button (selected[0])
				i := 0
				for selected[i] >= numButtons-1-i {
					i++ // seek a selected[.] that may be changed (increased)
				}
				selected[i]++ // switch to 'next button' for that selected[.]
				for i--; i >= 0; i-- {
					// update previous selected[.] according to combination rule
					selected[i] = selected[i+1] + 1
				}
			}
		}
	}
	log.Fatalln("Unsolvable problem.")
	return -1
}
