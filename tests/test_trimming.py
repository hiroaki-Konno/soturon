from core.score_pos import Coordinate, ScorePosition

print("=== Coordinate.from_pixels ===")
c1 = Coordinate.from_pixels(169, 372)
print(f"  repr   : {c1}")
print(f"  .x, .y : {c1.x}, {c1.y}")
print(f"  resolve: {c1.resolve()}")

print("\n=== Coordinate.from_ratio ===")
# 169/854≒0.198, 372/480≒0.775 なので 854x480 で解決すると from_pixels に近い値になるはず
c2 = Coordinate.from_ratio(169/854, 372/480)
print(f"  repr              : {c2}")
print(f"  resolve(854, 480) : {c2.resolve(854, 480)}")
print(f"  resolve(1920,1080): {c2.resolve(1920, 1080)}")

print("\n=== from_ratio で .x にアクセスした場合のエラー確認 ===")
try:
    _ = c2.x
except AttributeError as e:
    print(f"  AttributeError: {e}")

print("\n=== from_ratio で resolve() を解像度なしで呼んだ場合のエラー確認 ===")
try:
    c2.resolve()
except ValueError as e:
    print(f"  ValueError: {e}")

print("\n=== ScorePosition.mock_get_pos ===")
for name in ScorePosition.mock_pos_dict:
    sp = ScorePosition.mock_get_pos(name)
    pos1 = sp.pos1.resolve()
    pos2 = sp.pos2.resolve()
    print(f"  {name}: pos1={pos1}, pos2={pos2}")
