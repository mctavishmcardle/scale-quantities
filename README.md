# Scaled Quantity Reference

Two problems I've encountered when considering scale modeling projects are:
* Given an object or scene, what is the smallest feature I can reasonably
  represent at a certain scale, given the tools & materials I have or am willing
  to acquire, & in for the range of features larger than that, what techniques,
  materials, or tools will I have to use to construct that representation?
* Given a scale and a certain set of tools, materials, & techniques, what sorts
  of objects scenes can I reasonably represent?

To help with those issues, this repo contains:
* A script for presenting a number of common objects & sizes and a range of
  scales, both representing the object at that scale (i.e., "how large would a
  feature have to be to represent this object at this scale?) and the object in
  that scale (i.e., "how large is this object, when used to build a feature in
  a scene modeled at this scale?")
* A materialized set of size values, pretty-printed for reasonably easy perusal

The set of inputs (scales & objects) is designed to make it easy to include (or
remove) another scale or object, for future expansion.

The calculation script  makes use of the `pint` library for unit handling, so
scales can be input as equivalency ratios (e.g. 5mm equals 1ft) & object sizes
can be input natively (e.g. the diameter of an M5 bolt does not first need to be
converted to inches, or vice versa). Because I am most conversant with US
customary units, the output list uses feet & inches, but modifying that to suit
another unit system would not be difficult.

# Development

This repo uses `pipenv` for managing the development environment.
