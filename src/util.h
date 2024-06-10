#pragma once

#include <bitset>
#include <cstring>
#include <iostream>
#include <limits>
#include <random>

template <typename T> void gen_random_overflowing_sum(T &a, T &b) {
  while (true) {
    static std::random_device rd;
    static std::mt19937 gen(rd());

    static std::uniform_real_distribution<T> dis(
        std::numeric_limits<T>::max() / 16, std::numeric_limits<T>::max());

    T num1 = dis(gen);
    T num2 = dis(gen);

    T sum = num1 + num2;

    if (sum == std::numeric_limits<T>::infinity()) {
      a = num1;
      b = num2;
      return;
    }
  }
}

template <typename T> void gen_random_uniform(T &a) {
  static std::random_device rd;
  static std::mt19937 gen(rd());

  static std::uniform_real_distribution<T> dis(std::numeric_limits<T>::min(),
                                               std::numeric_limits<T>::max());

  a = dis(gen);
}

template <typename T> void gen_random_normal(T &a) {
  static std::random_device rd;
  static std::mt19937 gen(rd());

  static std::normal_distribution<T> dis(static_cast<T>(0.0),
                                         static_cast<T>(200000.0));

  a = dis(gen);
}

template <typename T> void print_bits_of_fp(T number) {
  unsigned long int bits;
  std::memcpy(&bits, &number, sizeof(T));
  constexpr size_t bitwidth = sizeof(T) * 8;
  std::bitset<bitwidth> bitset(bits);
  std::cout << bitset;
}