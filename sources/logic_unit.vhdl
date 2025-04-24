entity logic_unit is
  port (
    a : in std_logic;
    b : in std_logic;
    y1 : out std_logic;
    y2 : out std_logic;
    y3 : out std_logic
  );
end logic_unit;

architecture rtl of logic_unit is
begin
  y1 <= a or b;
  y2 <= a xor b;
  y3 <= not a;
end rtl;
