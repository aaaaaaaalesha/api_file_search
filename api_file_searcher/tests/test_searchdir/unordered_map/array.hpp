// Copyright 2020 aaaaaaaalesha <sks2311211@mail.ru>

#ifndef INCLUDE_ARRAY_HPP_
#define INCLUDE_ARRAY_HPP_

#include <algorithm>

template<class T>
class Array {
private:
    size_t size_;
    T *arr_;

public:
    Array() : size_(0) { arr_ = new T[1]; }

    ~Array() { delete[] arr_; }

    Array(size_t size, const T &value) : size_(size) {
        arr_ = new T[size];
        std::fill(arr_, arr_ + size, value);
    }

    Array(const Array &oth) : size_(oth.size_) {
        arr_ = new T[oth.size_];
        std::copy(oth.arr_, oth.arr_ + oth.size_, arr_);
    }

    Array &operator=(const Array &rhs) {
        if (this != &rhs) {
            size_ = rhs.size_;

            auto *newArr = new T[rhs.size_];
            std::copy(rhs.arr_, rhs.arr_ + size_, newArr);

            delete[] arr_;
            arr_ = newArr;
        }
        return *this;
    }

    T &operator[](size_t index) const { return arr_[index]; }

    T &operator[](size_t index) { return arr_[index]; }

    const T *data() const { return arr_; }

    T *data() noexcept { return arr_; }

    size_t size() const noexcept { return size_; }
};

#endif  // INCLUDE_ARRAY_HPP_
