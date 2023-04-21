// Copyright 2021 aaaaaaaalesha

#ifndef INCLUDE_ARRAY_HPP_
#define INCLUDE_ARRAY_HPP_

#include <algorithm>

template<class T>
class Array {
private:
    size_t size_;
    size_t capacity_;
    T *arr_;

public:
    Array() : size_(0u), capacity_(1u), arr_(new T[1]) {}

    ~Array() {
        delete[] arr_;
        arr_ = nullptr;
    }

    explicit Array(size_t capacity)
            : size_(0u), capacity_(capacity), arr_(new T[capacity]) {}

    Array(size_t size, const T &value)
            : size_(size), capacity_(size), arr_(new T[size]) {
        std::fill(arr_, arr_ + size, value);
    }

    Array(const Array &oth)
            : size_(oth.size_), capacity_(oth.capacity_), arr_(new T[oth.capacity_]) {
        std::copy(oth.arr_, oth.arr_ + oth.size_, arr_);
    }

    Array &operator=(const Array &rhs) {
        if (this != &rhs) {
            size_ = rhs.size_;
            capacity_ = rhs.capacity_;

            auto *newArr = new T[rhs.capacity_];
            std::copy(rhs.arr_, rhs.arr_ + size_, newArr);

            delete[] arr_;
            arr_ = newArr;
        }
        return *this;
    }

    const T &operator[](size_t index) const { return arr_[index]; }

    T &operator[](size_t index) { return arr_[index]; }

    const T *data() const { return arr_; }

    T *data() noexcept { return arr_; }

    void push_back(const T &value) {
        if (capacity_ <= size_) {
            throw std::logic_error("Array should be with fixed capacity.");
        }
        arr_[size_] = value;
        ++size_;
    }

    T pop_back() {
        --size_;
        return arr_[size_];
    }

    void resize(size_t size) {
        if (size > capacity_) {
            throw std::logic_error("Array should be with fixed capacity.");
        }
        size_ = size;
    }

    size_t size() const noexcept { return size_; }

    void clear() { return resize(0u); }

    bool empty() const { return size_ == 0u; }
};

#endif  // INCLUDE_ARRAY_HPP_