#define NODE_H
#ifndef NODE_H

#include <map>


class Node {

public:
	Node();

    void setName(std::string name);
    std::string getName();

private:
    std::string name;
    std::map<std::string, std::string> param;

    Node node[];
};

#endif // NODE_H
