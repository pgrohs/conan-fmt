#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class FmtConan(ConanFile):
    name = "fmt"
    version = "4.1.0"
    license = "https://github.com/fmtlib/fmt/blob/master/LICENSE.rst"
    url = "https://github.com/bincrafters/conan-fmt"
    homepage = "https://github.com/fmtlib/fmt"
    description = "A safe and fast alternative to printf and IOStreams."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "header_only": [True, False]}
    default_options = "shared=False", "header_only=False"
    exports = ["LICENSE.md"]
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'

    def config_options(self):
        if self.options.header_only:
            self.settings.clear()
            self.options.remove("shared")

    def source(self):
        source_url = "https://github.com/fmtlib/fmt"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        os.rename("fmt-{0}".format(self.version), "sources")

    def build(self):
        if not self.options.header_only:
            cmake = CMake(self)
            cmake.definitions["FMT_TEST"] = False
            cmake.definitions["FMT_INSTALL"] = True
            cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
            cmake.configure()
            cmake.build()
            cmake.install()

    def package(self):
        self.copy("license*", dst="licenses", src=os.path.join("sources"), ignore_case=True, keep_path=False)
        if self.options.header_only:
            self.copy("*.h", src=os.path.join("sources", "fmt"), dst=os.path.join("include", "fmt"))
            self.copy("*.cc", src=os.path.join("sources", "fmt"), dst=os.path.join("include", "fmt"))

    def package_info(self):
        if self.options.header_only:
            self.info.header_only()
        else:
            self.cpp_info.libs = ["fmt"]

        if self.options.shared and not self.options.header_only:
            self.cpp_info.bindirs.append("lib")
