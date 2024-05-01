import dataclasses
import pickle

from typing import Any, List, Optional


@dataclasses.dataclass
class UniformState:
    name: str
    fmt: str
    value: Any
    min_value: float
    max_value: float


@dataclasses.dataclass
class RaveState:
    uniform_values: List[UniformState]
    fragment_shader_source_code: str

    @staticmethod
    def load(path: str) -> Optional[RaveState]:
        try:
            with open(path, "rb") as fp:
                state = pickle.load(fp)
                return state
        except:
            print("Failed to load RAVE Project file")
            return None

    def save(
        self, uniform_values: List[UniformState], fragment_shader_source_code: str
    ) -> bool:
        try:
            state = RaveState(uniform_values, fragment_shader_source_code)

            with open(path, "wb") as fp:
                pickle.dump(state, fp)

            return True
        except:
            print("Failed to save RAVE Project file")
            return False


if __name__ == "__main__":
    import moderngl

    u1 = UniformState("timeScale", "1f", 1.0, 0.0, 5.0)
    u2 = UniformState("greenBlue", "2f", (0.5, 1.0), 0.0, 1.0)
    fragment_shader_source_code = """#version 330 core
    
    uniform float u_time;
    uniform float timeScale;
    uniform vec2 greenBlue;

    out vec4 fragColor;

    void main()
    {
        fragColor = vec4(mod(u_time * timeScale, 1.0), greenBlue.x, greenBlue.y, 1.0);
    }
    """

    s = RaveState([u1, u2], fragment_shader_source_code)

    with open("test.raveproj", "wb") as fp:
        pickle.dump(s, fp)

    with open("test.raveproj", "rb") as f:
        l = pickle.load(f)

    print(l)
