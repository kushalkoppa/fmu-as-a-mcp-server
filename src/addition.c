/**
 * addition.c - Implementation of addition function
 * 
 * This file implements the addition function for the Virtual ECU FMU.
 * The addition operation is a core arithmetic capability of the ECU.
 */

#include "addition.h"

/**
 * Add two numbers
 * 
 * @param a First number to add
 * @param b Second number to add
 * @return The sum of a and b
 */
double add(double a, double b) {
    return a + b;
}
