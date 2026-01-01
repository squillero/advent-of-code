// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package algorithm

import (
	"github.com/squillero/advent-of-code/2025/go/day10/data"
)

// Local (unexported module only) variables
var currentMachine *data.Machine
var selectedButtons []int
var bestSolutionButtons int
