#!/usr/bin/env ruby

s = STDIN.read
n = s.length

i = 1
s.each_char {|c|
  if c.ord < 128 or rand(n) < i then
    print "#{c}"
  end
  i += 1
}
