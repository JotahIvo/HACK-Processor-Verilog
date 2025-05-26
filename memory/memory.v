// Memory.v
module Memory (
    input         clk,
    input  [15:0] in,
    input         load,
    input  [14:0] address,
    output reg [15:0] out
);
  // RAM 0x0000–0x3FFF
  reg [15:0] ram [0:16383];
  // Screen 0x4000–0x5FFF
  reg [15:0] screen [0:8191];
  // Keyboard 0x6000
  reg [15:0] keyboard;

  // leitura combinacional
  always @(*) begin
    if      (address < 15'd16384)      out = ram[address];
    else if (address < 15'd24576)      out = screen[address-15'd16384];
    else if (address == 15'd24576)     out = keyboard;
    else                                out = 16'h0000;
  end

  // escrita síncrona
  always @(posedge clk) begin
    if (load) begin
      if      (address < 15'd16384)      ram[address]         <= in;
      else if (address < 15'd24576)      screen[address-15'd16384] <= in;
      else if (address == 15'd24576)     keyboard            <= in;
    end
  end
endmodule
