// Copyright 2021 aaaaaaaalesha

#ifndef INCLUDE_UNROLLED_LINKED_LIST_HPP_
#define INCLUDE_UNROLLED_LINKED_LIST_HPP_

#include <iomanip>
#include <iostream>
#include <stack>
#include <stdexcept>
#include <utility>

#include "iterator.hpp"

template<class T, size_t BucketCapacity = unrolled_details::default_capacity>
class unrolled_linked_list;

template<class T, size_t BucketCapacity = unrolled_details::default_capacity>
std::ostream &operator<<(std::ostream &out,
                         const unrolled_linked_list<T, BucketCapacity> &ull) {
    for (auto *node = ull.head_; node != nullptr; node = node->next_) {
        out << "( [";
        for (size_t i = 0; i < BucketCapacity; ++i) {
            out << std::setw(5);
            if (i < node->size_) {
                out << node->bucket_[i];
            } else {
                out << "_";
            }
            if (i + 1 < BucketCapacity) {
                out << ", ";
            }
        }
        out << " ] ) --> ";
    }
    std::cout << "NULL" << std::endl;
    return out;
}

template<class T, size_t BucketCapacity>
class unrolled_linked_list {
private:
    using ValueType = T;
    using SizeType = size_t;

    using iterator = Iterator<ValueType, BucketCapacity>;
    using const_iterator = const iterator;
    using reference = ValueType &;
    using const_reference = const ValueType &;

    Node<ValueType, BucketCapacity> *head_ = nullptr;

    friend std::ostream &operator
    <<<T, BucketCapacity>(
    std::ostream &out,
    const unrolled_linked_list &ull
    );

    void CleanMemory() {
        if (head_ == nullptr) return;

        auto *node_deleter = head_;
        for (auto *forward_node = node_deleter->next_; forward_node != nullptr;
             node_deleter = forward_node, forward_node = forward_node->next_) {
            delete node_deleter;
        }
        delete node_deleter;
    }

public:
    /// Default constructor.
    unrolled_linked_list() = default;

    /// Destructor.
    ~unrolled_linked_list() { CleanMemory(); }

    /// Copy constructor.
    unrolled_linked_list(const unrolled_linked_list &oth) {
        CleanMemory();

        if (oth.head_ == nullptr) return;

        head_ = new Node<ValueType, BucketCapacity>{};
        auto *node_inserter = head_;
        auto *node = oth.head_;

        for (auto *forward_node = node->next_; forward_node != nullptr;
             node = forward_node, forward_node = forward_node->next_,
             node_inserter = node_inserter->next_) {
            node_inserter->size_ = node->size_;
            node_inserter->bucket_ = node->bucket_;
            node_inserter->next_ = new Node<ValueType, BucketCapacity>{};
        }

        node_inserter->size_ = node->size_;
        node_inserter->bucket_ = node->bucket_;
        node_inserter->next_ = nullptr;
    }

    /// Move constructor.
    unrolled_linked_list(unrolled_linked_list &&oth) noexcept: head_(nullptr) {
        head_ = oth.head_;
        oth.head_ = nullptr;
    }

    /// std::initializer_list constructor.
    unrolled_linked_list(std::initializer_list <ValueType> init_list)
            : head_(new Node<ValueType, BucketCapacity>{}) {
        for (const auto &e : init_list) {
            push_back(e);
        }
    }

    /// Copy assignment operator.
    unrolled_linked_list &operator=(const unrolled_linked_list &oth) {
        if (&oth != this) {
            CleanMemory();

            if (oth.head_ == nullptr) {
                return *this;
            }

            head_ = new Node<ValueType, BucketCapacity>{};
            auto *node_inserter = head_;
            auto *node = oth.head_;

            for (auto *forward_node = node->next_; forward_node != nullptr;
                 node = forward_node, forward_node = forward_node->next_,
                 node_inserter = node_inserter->next_) {
                node_inserter->size_ = node->size_;
                node_inserter->bucket_ = node->bucket_;
                node_inserter->next_ = new Node<ValueType, BucketCapacity>{};
            }

            node_inserter->size_ = node->size_;
            node_inserter->bucket_ = node->bucket_;
            node_inserter->next_ = nullptr;
        }

        return *this;
    }

    /// Move assignment operator.
    unrolled_linked_list &operator=(unrolled_linked_list &&oth) noexcept {
        if (&oth != this) {
            CleanMemory();
            head_ = oth.head_;
            oth.head_ = nullptr;
        }

        return *this;
    }

    const_reference operator[](size_t pos) const {
        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
            if (pos + 1 > node->size_) {
                pos -= node->size_;
            } else {
                return node->bucket_[pos];
            }
        }

        return node->bucket_[pos];
    }

    reference operator[](size_t pos) {
        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
            if (pos + 1 > node->size_) {
                pos -= node->size_;
            } else {
                return node->bucket_[pos];
            }
        }

        return node->bucket_[pos];
    }

    const_reference at(size_t pos) const {
        if (pos >= size()) {
            throw std::out_of_range("Position is out of range.");
        }

        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
            if (pos + 1 > node->size_) {
                pos -= node->size_;
            } else {
                return node->bucket_[pos];
            }
        }

        return node->bucket_[pos];
    }

    reference at(size_t pos) {
        if (pos >= size()) {
            throw std::out_of_range("Position is out of range.");
        }

        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
            if (pos + 1 > node->size_) {
                pos -= node->size_;
            } else {
                return node->bucket_[pos];
            }
        }

        return node->bucket_[pos];
    }

    iterator begin() {
        if (empty()) return iterator{};

        return iterator(head_->bucket_.data(), 0u, head_);
    }

    const_iterator begin() const {
        if (empty()) return const_iterator{};

        return const_iterator(head_->bucket_.data(), 0u, head_);
    }

    iterator end() {
        if (empty()) return begin();

        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
        }

        return iterator(node->bucket_.data() + node->size_, node->size_, node);
    }

    const_iterator end() const {
        if (empty()) return begin();

        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
        }

        return const_iterator(node->bucket_.data() + node->size_, node->size_,
                              node);
    }

    SizeType size() const {
        SizeType size = 0u;
        for (auto *node = head_; node != nullptr; node = node->next_) {
            size += node->size_;
        }
        return size;
    }

    void swap(unrolled_linked_list &oth) { std::swap(oth, *this); }

    void clear() { unrolled_linked_list{}.swap(*this); }

    SizeType bucket_capacity() const { return BucketCapacity; }

    SizeType empty() const { return head_ == nullptr; }

    const_reference front() const { return head_->bucket_[0]; }

    reference front() { return head_->bucket_[0]; }

    const_reference back() const {
        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
        }

        return node->bucket_[node->size_ - 1];
    }

    reference back() {
        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
        }

        return node->bucket_[node->size_ - 1];
    }

    void push_back(const T &value) {
        if (head_ == nullptr) {
            head_ = new Node<ValueType, BucketCapacity>{};
        }

        auto *node = head_;
        for (; node->next_ != nullptr; node = node->next_) {
        }

        if (node->size_ < BucketCapacity) {
            node->bucket_.push_back(value);
            ++(node->size_);
        } else {
            auto *new_node = new Node<ValueType, BucketCapacity>{};
            SizeType half_bucket_size = BucketCapacity / 2;

            // A half of elements from prev node moves to new_node.
            for (size_t i = half_bucket_size; i < BucketCapacity; ++i) {
                new_node->bucket_.push_back(node->bucket_[i]);
            }
            node->bucket_.resize(half_bucket_size);
            node->size_ = half_bucket_size;

            new_node->bucket_.push_back(value);
            new_node->size_ = new_node->bucket_.size();

            node->next_ = new_node;
            new_node->next_ = nullptr;
        }
    }

    T pop_back() {
        // If where is 1 node in list.
        if (head_->next_ == nullptr) {
            --head_->size_;
            T value = head_->bucket_.pop_back();
            if (head_->size_ == 0u) {
                delete head_;
                head_ = nullptr;
            }
            return value;
        }

        // Go to the 2 back nodes in list.
        auto *node = head_;
        auto forward_node = head_->next_;
        for (; forward_node->next_ != nullptr;
               node = forward_node, forward_node = forward_node->next_) {
        }

        T value = forward_node->bucket_.pop_back();
        --(forward_node->size_);

        if (forward_node->size_ == 0u) {
            node->next_ = nullptr;
            delete forward_node;
            forward_node = nullptr;
            return value;
        }

        // If last bucket's size < N/2 we should take elements from the previous
        // one.
        if (forward_node->size_ * 2 < BucketCapacity) {
            // We need to create stack like a suitable temp FILO storage.
            std::stack <T> bucket_stack;

            // If prev node's size less N/2 we'll merge our buckets.
            if (node->size_ * 2 <= BucketCapacity) {
                for (; forward_node->size_ != 0u; --(forward_node->size_)) {
                    bucket_stack.push(forward_node->bucket_.pop_back());
                }
                delete forward_node;
                forward_node = nullptr;

                while (!bucket_stack.empty()) {
                    node->bucket_.push_back(bucket_stack.top());
                    ++node->size_;
                    bucket_stack.pop();
                }

                node->next_ = nullptr;

                return value;
            }

            // Take all elements for last bucket.
            while (!forward_node->bucket_.empty()) {
                bucket_stack.push(forward_node->bucket_.pop_back());
            }

            // Take needed elements for previous bucket.
            while (node->bucket_.size() * 2 > BucketCapacity) {
                bucket_stack.push(node->bucket_.pop_back());
                --node->size_;
            }

            forward_node->bucket_.resize(0);

            while (!bucket_stack.empty()) {
                forward_node->bucket_.push_back(bucket_stack.top());
                bucket_stack.pop();
            }
            forward_node->size_ = forward_node->bucket_.size();
        }

        return value;
    }

    iterator insert(const_iterator pos, const ValueType &value) {
        // If container is empty.
        if (empty()) {
            head_ = new Node<ValueType, BucketCapacity>{};
            head_->bucket_.push_back(value);
            ++head_->size_;

            return iterator(head_->bucket_.data(), 0u, head_);
        }

        auto node = pos.node_ptr_;
        // If the bucket isn't full.
        if (node->size_ < BucketCapacity) {
            // If pos is last of the bucket.
            if (pos.index_ == node->size_ - 1) {
                node->bucket_[pos.index_ + 1] = value;
                ++node->size_;
                node->bucket_.resize(node->size_);

                return iterator(node->bucket_.data() + pos.index_ + 1, pos.index_ + 1,
                                node);
            }

            // Otherwise.
            std::stack <ValueType> bucket_stack;
            for (auto i = pos.index_ + 1; i != node->size_; ++i) {
                bucket_stack.push(node->bucket_[i]);
            }
            for (size_t i = node->size_; !bucket_stack.empty(); --i) {
                node->bucket_[i] = bucket_stack.top();
                bucket_stack.pop();
            }

            node->bucket_[pos.index_ + 1] = value;
            ++node->size_;
            node->bucket_.resize(node->size_);

            return iterator(pos.ptr_ + 1, pos.index_ + 1, node);
        }

        // If bucket is going to be overflow.
        auto *new_node = new Node<ValueType, BucketCapacity>{};
        new_node->bucket_.push_back(value);
        ++new_node->size_;
        size_t right_slice_idx = pos.index_ + 1;
        // If pos is last of the bucket.
        if (right_slice_idx == BucketCapacity) {
            new_node->next_ = node->next_;
            node->next_ = new_node;
            return iterator(new_node->bucket_.data(), 0u, new_node);
        }

        // A half of elements from prev node moves to new_node.
        for (size_t i = right_slice_idx; i < BucketCapacity; ++i) {
            new_node->bucket_.push_back(node->bucket_[i]);
        }
        node->bucket_.resize(right_slice_idx);
        node->size_ = right_slice_idx;
        new_node->size_ = new_node->bucket_.size();

        new_node->next_ = node->next_;
        node->next_ = new_node;

        return iterator(new_node->bucket_.data(), 0u, new_node);
    }

    iterator erase(const_iterator pos) {
        std::stack <ValueType> bucket_stack;
        auto node = pos.node_ptr_;

        // If is there 1 element in node, node would be destructed.
        if (node->size_ == 1u) {
            // If last node is head.
            if (node == head_) {
                head_ = head_->next_;
                delete node;
                node = nullptr;
                return begin();
            }

            // Find the previous node.
            auto prev_node = head_;
            for (; prev_node->next_ != node; prev_node = prev_node->next_) {
            }
            prev_node->next_ = node->next_;
            delete node;
            node = nullptr;

            if (prev_node->next_ == nullptr) {
                return end();
            } else {
                return iterator(prev_node->next_->bucket_.data(), 0u, prev_node->next_);
            }
        }

        // If node's size > N/2.
        if (node->size_ * 2 > BucketCapacity) {
            while (pos.index_ + 1 != node->bucket_.size()) {
                bucket_stack.push(node->bucket_.pop_back());
            }
            --node->size_;
            for (size_t i = pos.index_; !bucket_stack.empty(); ++i) {
                node->bucket_[i] = bucket_stack.top();
                bucket_stack.pop();
            }

            node->bucket_.resize(node->size_);

            return iterator(pos.ptr_, pos.index_, node);
        }

        // Otherwise.
        // If pos in head.
        if (node == head_) {
            for (size_t i = pos.index_; i + 1 < node->size_; ++i) {
                node->bucket_[i] = node->bucket_[i + 1];
            }
            --node->size_;
            node->bucket_.resize(node->size_);

            return iterator(pos.ptr_, pos.index_, node);
        }

        // Find the previous node.
        auto prev_node = head_;
        for (; prev_node->next_ != node; prev_node = prev_node->next_) {
        }

        size_t half_bucket_size = BucketCapacity / 2;

        // If we can take elements from previous node. (size > N/2)
        if (prev_node->size_ > half_bucket_size &&
            node->size_ <= half_bucket_size) {
            // Take all elements, except for pos, for current bucket.
            while (!node->bucket_.empty()) {
                if (pos.index_ != node->bucket_.size() - 1) {
                    bucket_stack.push(node->bucket_.pop_back());
                } else {
                    node->bucket_.pop_back();
                }
            }

            // Save it to create iterator.
            size_t prev_taken_count = 0u;
            // Take needed elements from previous bucket.
            for (; prev_node->size_ != half_bucket_size; --prev_node->size_) {
                bucket_stack.push(prev_node->bucket_.pop_back());
                ++prev_taken_count;
            }

            // Push all elements from stack to bucket.
            while (!bucket_stack.empty()) {
                node->bucket_.push_back(bucket_stack.top());
                bucket_stack.pop();
            }
            node->size_ = node->bucket_.size();

            if (pos.index_ == node->size_) {
                if (node->next_ == nullptr) {
                    return end();
                } else {
                    return iterator(node->next_->bucket_.data(), 0u, node->next_);
                }
            }

            return iterator(pos.ptr_ + prev_taken_count,
                            pos.index_ + prev_taken_count, node);
        }

        for (size_t i = pos.index_; i + 1 < node->size_; ++i) {
            node->bucket_[i] = node->bucket_[i + 1];
        }
        --node->size_;
        node->bucket_.resize(node->size_);

        if (pos.index_ == node->size_) {
            if (node->next_ == nullptr) {
                return end();
            } else {
                return iterator(node->next_->bucket_.data(), 0u, node->next_);
            }
        }

        return iterator(pos.ptr_, pos.index_, node);
    }
};

#endif  // INCLUDE_UNROLLED_LINKED_LIST_HPP_