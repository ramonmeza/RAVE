import pickle

from dataclasses import dataclass, field
from typing import Any, List


# constants
DEFAULT_VERTEX_SHADER_SOURCE_CODE: str = """#version 330 core

in vec3 in_position;
in vec2 in_texcoord_0;

out vec2 uv0;

void main()
{
    gl_Position = vec4(in_position, 1.0);
    uv0 = in_texcoord_0;
}
"""

DEFAULT_FRAGMENT_SHADER_SOURCE_CODE: str = """#version 330 core

// RAVE provided uniforms
uniform float rTime;

// user specified uniforms
uniform float uTimeScale;
uniform float rAudioRMS;
uniform float rAudioFFT[512];

// output
out vec4 fragColor;

void main()
{
    fragColor = vec4(mod(rTime * uTimeScale, 1.0), mod(rAudioRMS, 1.0), mod(rAudioFFT[0], 1.0), 1.0);
}
"""


@dataclass
class UniformField:
    """Represents an OpenGL Uniform value, along with min and max values specified by the user."""

    name: str = ""
    """Name of the Uniform."""

    fmt: str = ""
    """Format of the Uniform."""

    value: Any = None
    """Current value of the Uniform."""

    min_value: float = 0.0
    """Minimum value for the Uniform, as specified by the user through the UI."""

    max_value: float = 1.0
    """Maximum value for the Uniform, as specified by the user through the UI."""


@dataclass
class Project:
    """Represents a RAVE project, including all uniform values and shader source code."""

    name: str = "My RAVE Project"
    """Name of the project."""

    author: str = "RAVER"
    """The person or group of people who worked on this project."""

    description: str = "A cool, real-time visualizer!"
    """Description of the project."""

    uniform_fields: List[UniformField] = field(default_factory=lambda: {})
    """A list of all uniforms and their values."""

    fragment_shader_source_code: str = DEFAULT_FRAGMENT_SHADER_SOURCE_CODE
    """Fragment shader source code for the project."""

    vertex_shader_source_code: str = DEFAULT_VERTEX_SHADER_SOURCE_CODE
    """Vertex shader source code for the project."""


def new_project() -> Project:
    return Project()


def load_project(path: str) -> Project:
    """Load a Project object from a file, using specified path.

    Args:
        path (str): Path to the file to load.

    Returns:
        Project: The loaded Project object
    """
    try:
        with open(path, "rb") as fp:
            project = pickle.load(fp)
            return project
    except:
        return None


def save_project(path: str, project: Project) -> bool:
    """Save the specified Project object to the given path.

    Args:
        path (str): Path to save the object to.
        project (Project): Project object to save.

    Returns:
        bool: Whether the saving process succeeded.
    """
    try:
        with open(path, "wb") as fp:
            pickle.dump(project, fp)
        return True
    except:
        return False
