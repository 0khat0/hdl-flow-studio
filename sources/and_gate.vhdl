entity and_gate is
    port (
      a : in std_logic;
      b : in std_logic;
      y : out std_logic
    );
  end and_gate;
  
  architecture rtl of and_gate is
  begin
    y <= a and b;
  end rtl;
  