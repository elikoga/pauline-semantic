{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  LD_LIBRARY_PATH = pkgs.lib.strings.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
    pkgs.protobufc
  ];

  packages = [
    pkgs.protobufc
  ];
}
