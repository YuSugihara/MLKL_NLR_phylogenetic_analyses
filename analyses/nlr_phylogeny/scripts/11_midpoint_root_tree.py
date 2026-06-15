#!/usr/bin/env python3
"""Midpoint-root a Newick tree with Biopython."""

from __future__ import annotations

import argparse

from Bio import Phylo


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_tree", help="Input Newick tree")
    parser.add_argument("output_tree", help="Output midpoint-rooted Newick tree")
    args = parser.parse_args()

    tree = Phylo.read(args.input_tree, "newick")
    tree.root_at_midpoint()
    Phylo.write(tree, args.output_tree, "newick")


if __name__ == "__main__":
    main()
