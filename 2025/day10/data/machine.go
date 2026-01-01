// Advent of Code 2025 | https://adventofcode.com/2025/day/10
// Copyright 2025 by Giovanni Squillero
// SPDX-License-Identifier: 0BSD

package data

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

type Button int
type Wiring []int
type Machine struct {
	LightDiagram        []bool
	ButtonWirings       []Wiring
	JoltageRequirements []int
}

func parseInts(token string) []int {
	var nums []int

	for _, t := range strings.Split(token, ",") {
		n, _ := strconv.Atoi(t)
		nums = append(nums, n)
	}
	return nums
}

func ReadFile(fileName string) []Machine {
	file, err := os.Open(fileName)
	if err != nil {
		log.Panicf("%v", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanWords)

	var newMachine Machine
	var machines []Machine
	for scanner.Scan() {
		word := scanner.Text()
		switch word[0] {
		case '[': // new machine
			newMachine = Machine{
				LightDiagram: make([]bool, len(word)-2),
			}
			for i, d := range word[1 : len(word)-1] {
				newMachine.LightDiagram[i] = d == '#'
			}
		case '(': // wirings
			newMachine.ButtonWirings = append(newMachine.ButtonWirings, parseInts(word[1:len(word)-1]))
		case '{': // joltage (last info)
			newMachine.JoltageRequirements = parseInts(word[1 : len(word)-1])
			machines = append(machines, newMachine)
		}
	}
	return machines
}
