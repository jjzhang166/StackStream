// The MIT License (MIT)
//
// Copyright (c) 2016 Erik Hvatum
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
// Authors: Erik Hvatum <ice.rikh@gmail.com>

#pragma once

#ifndef QT_NO_DEBUG
 #define QT_QML_DEBUG
#endif

#include <QEnableSharedFromThis>
#include <QSharedDataPointer>
#include <QtCore>
#include <QtGui>
#include <QtPlugin>
#include <QProcess>
#include <QSharedPointer>
#include <QtQml>
#include <QtQuick>
#include <QtQuick/qsggeometry.h>
#include <QtQuick/qsgnode.h>
#include <QtQuick/qsgtexture.h>
#include <QtQuick/qsgtextureprovider.h>
#include <QtWidgets>
#include <atomic>
#include <cstdint>
#include <forward_list>
#include <limits>
#include <memory>
#include <stdexcept>
#include <string>

#ifdef WITH_PYTHON
 #include <Python.h>
#endif

#ifdef STACKSTREAM
 #define STACKSTREAM_DLLSPEC Q_DECL_EXPORT
 #ifdef ENABLE_GL_DEBUG_LOGGING
  extern QOpenGLDebugLogger* g_glDebugLogger;
 #endif
#else
 #define STACKSTREAM_DLLSPEC Q_DECL_IMPORT
#endif

#ifdef min
 #undef min
#endif

#ifdef max
 #undef max
#endif

#ifdef read
 #undef read
#endif

#ifdef write
 #undef write
#endif

#include <chrono>
#include <iostream>
#include <iomanip>

class TimeThisBlock
{
public:
    TimeThisBlock() : t0(std::chrono::high_resolution_clock::now()) {}
    ~TimeThisBlock()
    {
        std::chrono::high_resolution_clock::time_point t1{std::chrono::high_resolution_clock::now()};
        double nanoseconds_elapsed = static_cast<double>(std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count());
        if(nanoseconds_elapsed < 1000)
            std::cout << nanoseconds_elapsed << "ns";
        else if(nanoseconds_elapsed < 1e6)
            std::cout << nanoseconds_elapsed * static_cast<double>(1e-3) << "µs";
        else if(nanoseconds_elapsed < 1e9)
            std::cout << nanoseconds_elapsed * static_cast<double>(1e-6) << "ms";
        else
            std::cout << nanoseconds_elapsed * static_cast<double>(1e-9) << "s";
        std::cout << std::endl;
    }
protected:
    std::chrono::high_resolution_clock::time_point t0;
};
