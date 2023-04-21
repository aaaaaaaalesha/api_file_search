// Copyright 2020 aaaaaaaalesha <sks2311211@mail.ru>

#ifndef INCLUDE_ITERATOR_HPP_
#define INCLUDE_ITERATOR_HPP_

#include <algorithm>
#include "array.hpp"
#include <initializer_list>
#include <iostream>
#include <list>
#include <memory>
#include <stdexcept>
#include <utility>

template <class KeyIt, class TIt>
class Iterator
    : public std::iterator<std::forward_iterator_tag, std::pair<KeyIt, TIt>> {
 private:
  using ValueType = std::pair<KeyIt, TIt>;
  using Table = Array<std::list<ValueType>>;
  using LocalIterator = typename std::list<ValueType>::iterator;

  Table *tableP_;
  LocalIterator localIterator_;
  size_t bucketIndex_;

  bool IsLocalEnd() {
    return localIterator_ == (tableP_->operator[](bucketIndex_)).end();
  }

  bool IsNextBucketEmpty() {
    return (tableP_->operator[](bucketIndex_ + 1)).empty();
  }

  bool IsLastBucket() { return (bucketIndex_ + 1) == tableP_->size(); }

 public:
  Iterator() : tableP_(nullptr), bucketIndex_(0) {}

  Iterator(const Iterator &it) = default;

  Iterator(const Table *table, size_t bucketIndex, LocalIterator localIterator)
      : tableP_(const_cast<Table *>(table)),
        localIterator_(localIterator),
        bucketIndex_(bucketIndex) {}

  Iterator &operator=(const Iterator rhs) {
    tableP_ = rhs.tableP_;
    localIterator_ = rhs.localIterator_;
    bucketIndex_ = rhs.bucketIndex_;

    return *this;
  }

  // Preincrement.
  Iterator &operator++() {
    if (!IsLocalEnd()) {
      ++localIterator_;
    }

    if (IsLocalEnd() && !IsLastBucket()) {
      while (!IsLastBucket() && IsNextBucketEmpty()) {
        ++bucketIndex_;
      }

      if (!IsLastBucket()) ++bucketIndex_;

      localIterator_ = (tableP_->operator[](bucketIndex_)).begin();
    }

    return *this;
  }

  // Postincrement.
  Iterator operator++(int) {
    Iterator prevState(*this);
    ++(*this);

    return prevState;
  }

  ValueType operator*() const { return *localIterator_; }

  ValueType &operator*() { return *localIterator_; }

  const ValueType *operator->() const { return &(*localIterator_); }

  ValueType *operator->() { return &(*localIterator_); }

  bool operator==(const Iterator rhs) const {
    return localIterator_ == rhs.localIterator_;
  }

  bool operator!=(const Iterator rhs) const {
    return localIterator_ != rhs.localIterator_;
  }
};

#endif  // INCLUDE_ITERATOR_HPP_
