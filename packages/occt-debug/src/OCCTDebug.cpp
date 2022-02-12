#include <pybind11/pybind11.h>

#include <opencascade/Standard_Real.hxx>

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(OCCTDebug, m) {
    m.def("add", &add, "A function that adds two numbers");

    // opencascade/Standard_Real.hxx
    m.def("arccos", &ACosApprox, "Returns the approximate value of the arc cosine of a real.");
}
