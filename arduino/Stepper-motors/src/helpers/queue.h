#ifndef Queue_H
#define Queue_H

/**
*Class of queue of pointers. NO pointer given to this queue will be deleted. Should be done somewhere else in the code.
*/
template <typename T>
class Queue
{

private:
    struct Element{
        T* element;
        Element* next = nullptr;

        Element(T* element, Element* previous):element(element)
        {
            if(previous)
                previous->next = this;
        }

        ~Element(){}// Do not delete pointer here
    };
    Element* head = nullptr;
    Element* tail = nullptr;

public:
    Queue(){};
    ~Queue();
    void add(T *i);
    void addFirst(T *i);
    T* pop();
    bool isEmpty();
};

#endif