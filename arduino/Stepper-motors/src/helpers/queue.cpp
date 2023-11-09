#include "queue.h"

template<typename T>
Queue<T>::~Queue()
{
    T *tmp;
    while (tmp = pop()){
      delete tmp;
    }
}

template<typename T>
void Queue<T>::add(T *i)
{
    tail = new Element(i, tail);
    if(!head){
      head = tail; // if queue was empty
    }
}

template<typename T>
void Queue<T>::addFirst(T *i)
{
    if(!tail){
      add(i); // if queue was empty
    }
    Element* newHead = new Element(i, nullptr);
    newHead->next = head;
    head->previous = newHead;
    head = newHead;
}

template<typename T>
T* Queue<T>::pop()
{
    if(isEmpty())return nullptr;
    T* res = head->element;
    Element* newHead = head->next;
    delete head;
    head = newHead;
    if(head==nullptr)tail=nullptr;
    return res;
}

template<typename T>
bool Queue<T>::isEmpty()
{
  return queue == nullptr;
}
