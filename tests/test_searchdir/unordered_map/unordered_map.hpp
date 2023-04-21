// Copyright 2020 aaaaaaaalesha <sks2311211@mail.ru>

#ifndef INCLUDE_UNORDERED_MAP_HPP_
#define INCLUDE_UNORDERED_MAP_HPP_

#include <algorithm>
#include "array.hpp"
#include <exception>
#include <functional>
#include <initializer_list>
#include <iostream>
#include "iterator.hpp"
#include <list>
#include <utility>
#include <vector>

namespace um_details {
const size_t defaultBucketCount = 9;
const float defaultMaxLoadFactor = 2.5;
const size_t rehashCoff = 2;
}  // namespace um_details

template <class Key, class T, class Hash = std::hash<Key>,
          class EqualKey = std::equal_to<Key>>
class UnorderedMap {
 public:
  using iterator = Iterator<Key, T>;

 private:
  using Table = Array<std::list<std::pair<Key, T>>>;
  using ValueType = std::pair<Key, T>;
  using SizeType = size_t;
  using LocalIterator = typename std::list<ValueType>::iterator;
  using ConstLocalIterator = const LocalIterator;

  SizeType bucketCount_;
  Table table_;
  Hash hasher_;
  EqualKey equalKey_;
  SizeType size_;

  SizeType BucketIndex(const Key &key) const {
    return hasher_(key) % bucketCount();
  }

 public:
  UnorderedMap()
      : bucketCount_(um_details::defaultBucketCount),
        table_(Table(bucketCount_, std::list<ValueType>{})),
        size_(0) {}

  UnorderedMap(std::initializer_list<ValueType> iList,
               SizeType bucketCount = um_details::defaultBucketCount,
               const Hash &hash = Hash(), const EqualKey &equal = EqualKey())
      : bucketCount_(bucketCount),
        table_(Table(bucketCount_, std::list<ValueType>{})),
        hasher_(hash),
        equalKey_(equal),
        size_(iList.size()) {
    for (const auto &e : iList) {
      insert(e);
    }
  }

  UnorderedMap(const std::vector<ValueType> &vec,
               SizeType bucketCount = um_details::defaultBucketCount,
               const Hash &hash = Hash(), const EqualKey &equal = EqualKey())
      : bucketCount_(bucketCount),
        table_(Table(bucketCount_, std::list<ValueType>{})),
        hasher_(hash),
        equalKey_(equal),
        size_(vec.size()) {
    for (const auto &e : vec) {
      insert(e);
    }
  }

  UnorderedMap(const UnorderedMap &oth)
      : bucketCount_(oth.bucketCount_),
        table_(oth.table_),
        hasher_(oth.hasher_),
        equalKey_(oth.equalKey_),
        size_(oth.size_) {}

  UnorderedMap(UnorderedMap &&oth) noexcept
      : bucketCount_(oth.bucketCount_),
        table_(oth.table_),
        hasher_(oth.hasher_),
        equalKey_(oth.equalKey_),
        size_(oth.size_) {
    oth.bucketCount_ = um_details::defaultBucketCount;
    oth.table_ = Table();
    oth.size_ = 0;
  }

  UnorderedMap &operator=(const UnorderedMap &rhs) = default;

  UnorderedMap &operator=(UnorderedMap &&rhs) noexcept {
    if (this != &rhs) {
      bucketCount_ = rhs.bucketCount_;
      size_ = rhs.size_;
      table_ = rhs.table_;

      rhs.bucketCount_ = um_details::defaultBucketCount;
      rhs.table_ = Table();
      rhs.size_ = 0;
    }

    return *this;
  }

  SizeType size() const { return size_; }

  SizeType bucketCount() const { return bucketCount_; }

  LocalIterator begin(SizeType n) { return table_[n].begin(); }

  ConstLocalIterator begin(SizeType n) const { return table_[n].begin(); }

  LocalIterator end(SizeType n) { return table_[n].end(); }

  ConstLocalIterator end(SizeType n) const { return table_[n].end(); }

  iterator begin() const {
    if (!empty()) {
      for (SizeType i = 0; i < bucketCount_; ++i) {
        if (!table_[i].empty()) {
          return iterator(&table_, i, begin(i));
        }
      }
    }

    return iterator(&table_, 0, begin(0));
  }

  iterator end() const {
    if (!empty()) {
      return iterator(&table_, bucketCount_ - 1, end(bucketCount_ - 1));
    }

    return begin();
  }

  bool empty() const { return size_ == 0; }

  T &operator[](const Key &key) {
    auto lf = loadFactor();
    auto mlf = maxLoadFactor();
    if (lf > mlf) rehash(bucketCount_ * um_details::rehashCoff);
    auto &cell = table_[BucketIndex(key)];
    auto cellIt = cell.begin();

    while (cellIt != cell.end()) {
      if (equalKey_(cellIt->first, key)) {
        return cellIt->second;
      }
      ++cellIt;
    }

    cell.emplace_back(key, T{});
    ++size_;

    return cell.back().second;
  }

  T &at(const Key &key) {
    auto &cell = table_[BucketIndex(key)];
    auto cellIt = cell.begin();

    while (cellIt != cell.end()) {
      if (equalKey_(cellIt->first, key)) {
        return cellIt->second;
      }
      ++cellIt;
    }

    throw std::out_of_range(
        "Entered key does not match the key of any element "
        "in the container.");
  }

  std::pair<iterator, bool> insert(const ValueType &value) {
    if (loadFactor() > maxLoadFactor())
      rehash(bucketCount_ * um_details::rehashCoff);
    SizeType bucketIndex = BucketIndex(value.first);
    auto &cell = table_[bucketIndex];
    auto cellIt = cell.begin();
    bool keyNotExists = true;

    while (cellIt != cell.end()) {
      if (equalKey_(cellIt->first, value.first)) {
        keyNotExists = false;
        break;
      }
      ++cellIt;
    }

    if (keyNotExists) {
      cell.push_front(value);
      ++size_;
      iterator it1(&table_, bucketIndex, cell.begin());

      return std::make_pair(it1, keyNotExists);
    } else {
      iterator it2(&table_, bucketIndex, cellIt);

      return std::make_pair(it2, keyNotExists);
    }
  }

  SizeType erase(const Key &key) {
    auto &cell = table_[BucketIndex(key)];
    auto cellIt = cell.begin();

    while (cellIt != cell.end()) {
      if (equalKey_(cellIt->first, key)) {
        cell.erase(cellIt);
        --size_;
        return 1;
      }
      ++cellIt;
    }

    return 0;
  }

  void swap(UnorderedMap &oth) { std::swap(*this, oth); }

  void clear() noexcept {
    for (SizeType i = 0; i < bucketCount_; ++i) {
      table_[i].clear();
    }
    size_ = 0;
  }

  iterator find(const Key &key) {
    auto &cell = table_[BucketIndex(key)];
    auto cellIt = cell.begin();

    while (cellIt != cell.end()) {
      if (equalKey_(cellIt->first, key)) {
        return iterator(&table_, BucketIndex(key), cellIt);
      }
      ++cellIt;
    }

    return end();
  }

  void rehash(SizeType n) {
    if (n <= bucketCount_) return;

    std::vector<ValueType> tempStorage(size_);
    for (const auto &e : *this) tempStorage.push_back(e);

    this->clear();

    *this = UnorderedMap(tempStorage, n);
  }

  float loadFactor() const noexcept {
    return size_ / static_cast<float>(bucketCount_);
  }

  float maxLoadFactor() const noexcept {
    return um_details::defaultMaxLoadFactor;
  };
};

#endif  // INCLUDE_UNORDERED_MAP_HPP_
