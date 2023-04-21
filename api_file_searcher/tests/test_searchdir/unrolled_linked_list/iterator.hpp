// Copyright 2021 aaaaaaaalesha

#ifndef INCLUDE_ITERATOR_HPP_
#define INCLUDE_ITERATOR_HPP_

#include <iterator>

#include "array.hpp"

namespace unrolled_details {
// The maximum number if elements in each array (node).
    constexpr size_t default_capacity = 8u;
}  // namespace unrolled_details

template<class T, size_t BucketCapacity = unrolled_details::default_capacity>
struct Node {
    using Bucket = Array<T>;

    // Count of elements in node.
    size_t size_ = 0u;
    // Block of elements.
    Bucket bucket_ = Bucket(BucketCapacity);
    // Pointer to the next node in list.
    Node *next_ = nullptr;
};

template<class T, size_t BucketCapacity>
class unrolled_linked_list;

template<class T, size_t BucketCapacity = unrolled_details::default_capacity>
class Iterator : public std::iterator<std::forward_iterator_tag, T> {
private:
    using ValueType = T;

    ValueType *ptr_ = nullptr;
    size_t index_ = 0u;

    Node<T, BucketCapacity> *node_ptr_ = nullptr;

    friend class unrolled_linked_list<ValueType, BucketCapacity>;

public:
    Iterator() = default;

    Iterator(const Iterator<ValueType, BucketCapacity> &it) = default;

    Iterator(T *ptr, size_t index, Node<T, BucketCapacity> *node_ptr)
            : ptr_(ptr), index_(index), node_ptr_(node_ptr) {}

    Iterator &operator=(const Iterator oth) {
        ptr_ = oth.ptr_;
        index_ = oth.index_;
        node_ptr_ = oth.node_ptr_;

        return *this;
    }

    Iterator &operator++() {
        if (index_ < node_ptr_->size_ - 1) {
            ++ptr_;
            ++index_;
            return *this;
        }

        if (node_ptr_->next_ != nullptr) {
            node_ptr_ = node_ptr_->next_;
            ptr_ = node_ptr_->bucket_.data();
            index_ = 0u;
            return *this;
        }

        ++ptr_;  // end()

        return *this;
    }

    Iterator operator++(int) {
        Iterator prev_state(*this);
        operator++();

        return prev_state;
    }

    ValueType operator*() const { return *ptr_; }

    ValueType &operator*() { return *ptr_; }

    const ValueType *operator->() const { return &(*ptr_); }

    ValueType *operator->() { return &(*ptr_); }

    bool operator==(const Iterator rhs) const { return ptr_ == rhs.ptr_; }

    bool operator!=(const Iterator rhs) const { return ptr_ != rhs.ptr_; }
};

#endif  // INCLUDE_ITERATOR_HPP_