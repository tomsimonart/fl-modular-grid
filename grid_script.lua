l = (ch < 8) and 1 or 2
if ch % 2 == 1 and self.lcc >= 0 then
    led_color(self.lcc, l, (p1 >> 2) * 255 // 31, (((p1 & 3) << 3) | (p2 >> 4)) * 255 // 31, (p2 & 13) * 255 // 15, 1)
end
if ch % 2 == 0 and p1 >= self.ci and p1 <= self.cx then
    if ch == 2 then
        for i = 0, 15 do
            led_value(i, 1, 0)
            led_value(i, 2, 0)
        end
    else
        self.lcc = p1 % 16
        led_value(self.lcc, l, p2)
    end
else
    self.lcc = -1
end