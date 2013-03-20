#!/usr/bin/env ruby
#
# gradually let through more and more non-ascii text

s = STDIN.read
n = s.length

i = 1
s.each_char {|c|
  if c.ord < 128 or rand(n) < i then
    print "#{c}"
  end
  i += 1
}
