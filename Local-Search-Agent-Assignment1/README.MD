# Hill-Climbing Local Search Agent

## Overview

This project implements an **AI agent using a hill-climbing local search approach** to solve a grid-based shape placement problem.

The agent must place a sequence of colored shapes onto a grid while minimizing conflicts and producing a valid final arrangement. Since there can be many possible combinations of positions, shapes, and colors, searching through every possible state would be inefficient.

Instead, the agent uses **local search** to evaluate possible next moves and continuously improve the current solution.

> **Key Takeaway:** Designed and implemented a hill-climbing local search agent that evaluates candidate states using an objective function, with multiple trials, restarts, and a fallback strategy to improve solution robustness.

---

## Problem

The objective is to place the available shapes onto a grid while satisfying the problem's constraints.

At any point, the agent has a **current state** consisting of:

- The current grid
- Shapes that have already been placed
- Positions of the placed shapes
- Current shape and color selections

The agent must decide **which move to make next**.

The main challenge is that the number of possible states grows quickly as the agent considers different shape positions and colors. Rather than exhaustively exploring the entire search space, the project uses a local search strategy to efficiently find an acceptable solution.

---

## Approach

The solution uses **hill-climbing local search**.

Hill climbing starts with a current state and searches its neighboring states for an improvement. The agent repeatedly moves toward states with better objective values.

The overall process is:

```text
             Current State
                   │
                   ▼
          Generate Candidate Moves
                   │
                   ▼
         Simulate Candidate Move
                   │
                   ▼
          Calculate Objective
                   │
                   ▼
          Compare Candidate States
                   │
                   ▼
          Select Better Move
                   │
                   ▼
            Update Current State
                   │
                   ▼
              Repeat Search
