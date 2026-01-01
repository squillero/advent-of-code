// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package algorithm

import (
	"log"

	"github.com/squillero/advent-of-code/2025/go/day10/data"
)

// Checks wether pressing the selected buttons match machine's Light Diagram
func validDiagram() bool {
	target := currentMachine.LightDiagram
	current := make([]bool, len(currentMachine.LightDiagram))
	for i := 0; i < len(selectedButtons)-1; i++ {
		for _, w := range currentMachine.ButtonWirings[selectedButtons[i]] {
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
func SelectButtons_part1(m *data.Machine) int {
	currentMachine = m // stop passing around the machine
	numButtons := len(currentMachine.ButtonWirings)

	for numSelected := 1; numSelected <= numButtons; numSelected++ {
		// using exactly n (numSelected) buttons out of numButtons
		// order does not matter, selecting a button twice is useless
		selectedButtons = make([]int, numSelected+1)
		for i := 0; i <= numSelected; i++ {
			selectedButtons[i] = numSelected - i - 1 // the (n+1)-th button in -1
		}

		for selectedButtons[numSelected] < 0 { // loop while (n+1)-th button is -1
			if validDiagram() {
				return numSelected
			}

			// selectedButtons: the buttons we want to press
			// rule: selectedButtons[i] > selectedButtons[j] if i < j -- it's a combination
			// Example: numButtons is 5; numSelected is 3
			//// selectedButtons = [4 3 0 -1] -> Press buttons: 4, 3, and 0
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
			if selectedButtons[0] < numButtons-1 {
				// change first button. eg. [3 1 0 -1] => [4 1 0 -1]
				selectedButtons[0]++
			} else {
				// can't pick 'next one' for the first button (selectedButtons[0])
				i := 0
				for selectedButtons[i] >= numButtons-1-i {
					i++ // seek a selectedButtons[.] that may be changed (increased)
				}
				selectedButtons[i]++ // switch to 'next button' for that selectedButtons[.]
				for i--; i >= 0; i-- {
					// update previous selectedButtons[.] according to combination rule
					selectedButtons[i] = selectedButtons[i+1] + 1
				}
			}
		}
	}
	log.Fatalln("Unsolvable problem.")
	return -1
}
