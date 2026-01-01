// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package algorithm

import (
	"log"

	"github.com/squillero/advent-of-code/2025/go/day10/data"
)

// Checks wether pressing the selected buttons match machine's Light Diagram
func lightsOk(machine *data.Machine, buttons []int) bool {
	target := machine.LightDiagram
	current := make([]bool, len(machine.LightDiagram))
	for _, b := range buttons {
		for _, w := range machine.ButtonWirings[b] {
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

// Select the minimum number of buttons to match LightDiagram
func SelectButtons(machine *data.Machine) int {
	numButtons := machine.NumButtons()

	for numSelected := 1; numSelected <= numButtons; numSelected++ {
		// using exactly n (numSelected) buttons out of numButtons
		selected := make([]int, numSelected+1)
		for i := 0; i <= numSelected; i++ {
			selected[i] = numSelected - i - 1 // the (n+1)-th button in -1
		}

		for selected[numSelected] < 0 { // loop while (n+1)-th button is -1
			if lightsOk(machine, selected[:numSelected]) {
				return numSelected
			}

			// selected: the buttons we want to press (it's a permutation!)
			// rule: selected[i] > selected[j] if i < j
			// Example: numButtons is 5; numSelected is 3
			//// selected = [4 3 0 -1] -> Press buttons: 4, 3, and 0
			//// who's next?
			//// 4 can't be increased (buttons are {0, 1, 2, 3, 4})
			//// 3 can't be increased (button[1] must be < button[0])
			//// first possibility: button[2] -> change 0 to 1
			//// then button[1] is set to button[2] + 1
			//// then button[0] is set to button[1] + 1
			//// select = [3 2 1 -1] -> Press buttons: 3, 2, and 1
			//// next will be: select = [4 2 1 -1] 
			//// next will be: select = [4 3 1 -1] 
			//// next will be: select = [4 3 2 -1] 
			//// then, finally: select = [3 2 1 0] (that's the end!) 
			if selected[4] < numButtons-1 {
				// eg. [3 1 0 -1] => [4 1 0 -1]
				selected[0]++
			} else {
				// can't pick 'next one' for the first button (selected[0])
				i := 0
				for selected[i] >= numButtons-1-i {
					i++
				}
				selected[i]++ // pick 'next one' for a button that may be changed
				for i--; i >= 0; i-- {
					// update previous buttons (according to rule)
					selected[i] = selected[i+1] + 1
				}
			}
		}
	}
	log.Fatalln("Unsolvable problem.")
	return -1
}
