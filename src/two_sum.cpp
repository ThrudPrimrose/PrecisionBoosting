#include "util.h"

#include <iostream>

// Compiled with -Wconversion and -Wsign-conversion

void two_sum(float a, float b, float &s, float &t) {
  s = a + b;
  float a_prime = s - b;
  float b_prime = s - a_prime;
  float delta_a = a - a_prime;
  float delta_b = b - b_prime;
  t = delta_a + delta_b;
}

constexpr uint repeats = 20;

int main() {
  std::cout << "Check 2 sum for 2 different floats (sum in double to avoid "
               "loss of precision): "
            << std::endl;
  for (uint i = 0; i < repeats; i++) {
    float a, b;
    gen_random_normal(a);
    gen_random_normal(b);

    float s, t;
    two_sum(a, b, s, t);

    double ad = static_cast<double>(a);
    double bd = static_cast<double>(b);

    double sumd = ad + bd;
    double upcasted_sum = static_cast<double>(s) + static_cast<double>(t);

    std::cout << sumd << "(";
    // print_bits_of_fp(sumd);
    std::cout << ")" << " == " << upcasted_sum << "(";
    // print_bits_of_fp(upcasted_sum);
    std::cout << ")? " << (sumd == upcasted_sum) << std::endl;
  }

  std::cout << "Check Oozaki Schemes's error terms (sum in double to avoid "
               "loss of precision): "
            << std::endl;
  for (uint i = 0; i < repeats; i++) {
    double ad, bd;
    gen_random_normal(ad);
    gen_random_normal(bd);

    float af, bf, delta_af, delta_bf, sumf1, sumf2;
    af = static_cast<float>(ad);
    bf = static_cast<float>(bd);
    delta_af = static_cast<float>(ad - static_cast<double>(af));
    delta_bf = static_cast<float>(bd - static_cast<double>(bf));

    sumf1 = af + bf;
    sumf2 = delta_af + delta_bf;

    double sumd = ad + bd;
    double upcasted_sum =
        static_cast<double>(sumf1) + static_cast<double>(sumf2);

    std::cout << sumd << " == " << upcasted_sum << "? "
              << (sumd == upcasted_sum)
              << ", difference: " << sumd - upcasted_sum << std::endl;
  }
}