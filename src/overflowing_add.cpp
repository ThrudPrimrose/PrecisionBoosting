#include <cassert>
#include <cmath>
#include <fenv.h>
#include <iostream>
#include <limits>

#include "util.h"

// #pragma STDC FENV_ACCESS ON
constexpr uint repeats = 10;

int main() {
  for (uint i = 0; i < repeats; i++) {
    float max_float = std::numeric_limits<float>::max();
    // I generate two numbers such that the sum will overflow
    float a;
    float b;
    gen_random_overflowing_sum(a, b);
    // This overflows result is +inf
    float sum = a + b;
    assert(sum == std::numeric_limits<float>::infinity());

    std::cout << std::numeric_limits<float>::max() << std::endl;
    std::cout << std::numeric_limits<float>::max() / 2 << std::endl;

    std::cout << "Overflow occurred: " << a << " + " << b << " = " << sum
              << std::endl;

    // For simplicity I will upcast the numbers and compute them as doubles
    // Casting up to doubles just pads 0 to precision and every exponent of fp32
    // is representible as an exponent of fp64 so it is totally fine.
    double ad = static_cast<double>(a);
    double bd = static_cast<double>(b);
    double sumd = ad + bd;
    print_bits_of_fp(sumd);
    std::cout << std::endl;

    if (sumd == std::numeric_limits<double>::infinity()) {
      std::cout << "Overflow occurred: " << ad << " + " << bd << " = " << sumd
                << std::endl;
    } else {
      std::cout << "No overflow: " << ad << " + " << bd << " = " << sumd
                << std::endl;
    }

    // Can set the rounding flag with the following calls, as defined in C
    // standard But it does not always mitigate the 2nd round of error create.
    // const int originalRounding = fegetround();
    // fesetround(FE_UPWARD);
    // fesetround(originalRounding);

    // Now let's do it with my scheme
    // Note: this code snippe assumes no underflow when a - delta_b. I need to
    // check the possibility
    float delta_b = std::numeric_limits<float>::max() - b;
    assert(a > delta_b);
    float diff = a - delta_b;
    // Diff holds the overflow value
    // Since we are in the next integer group, we have an offset of
    // std::numeric_limits<float>::max()
    double diffd = static_cast<double>(diff) +
                   static_cast<double>(std::numeric_limits<float>::max());

    // Let's see the new value
    std::cout << diffd << std::endl;
    print_bits_of_fp(diffd);
    std::cout << std::endl;
    if (sumd == diffd) {
      std::cout << "Results equal: " << diffd << " == " << sumd << std::endl;
    } else {
      std::cout << "Results not equal " << diffd << " != " << sumd << std::endl;
    }
  }

  return 0;
}
