# -*- coding: utf-8 -*-

import sys
import math
import decimal
from cgrigvendor.six.moves import range

AXIS = {"x": 0, "y": 1, "z": 2}


def lerp(current, goal, weight=0.5):
    return (goal * weight) + ((1.0 - weight) * current)


def lerpCount(start, end, count):
    """Iterates between start and goal for the given count.

    .. code-block:: python

        for i in lerpCount(-10, 10, 8):
            print(i)

    Outputs::

        # 0.0
        # 0.25
        # 0.5
        # 0.75
        # 1.0

    :param start: The starting number i.e. 0.0
    :type start: float
    :param end: The goal number i.e. 1.0
    :type end: float
    :param count: The number of iterations.
    :type count: int
    :rtype: Iterable[float]
    """
    primaryFraction = (float(end) - float(start)) / float(count - 1)

    multiplier = start + primaryFraction
    yield start
    for n in range(count - 2):
        yield multiplier
        multiplier += primaryFraction
    yield end


def remap(value, oldMin, oldMax, newMin, newMax):
    return (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin


def almostEqual(x, y, tailCount):
    return (
            math.fabs(x - y) < sys.float_info.epsilon * math.fabs(x + y) * tailCount
            or math.fabs(x - y) < sys.float_info.min
    )


def mean(
        numbers,
):  # because we have to use py2 as well otherwise statistics stdlib module would be better
    """Returns the mean/average of the numbers.

    :param numbers: The numbers to average.
    :type numbers: list[float]
    :rtype: float
    """
    return float(sum(numbers)) / max(len(numbers), 1)


def threePointParabola(a, b, c, iterations):
    positions = []
    for t in range(1, int(iterations)):
        x = t / iterations
        q = b + (b - a) * x
        r = c + (c - b) * x
        p = r + (r - q) * x
        positions.append(p)
    return positions


def clamp(value, minValue=0.0, maxValue=1.0):
    """Clamps a value withing a max and min range

    :param value: value/number
    :type value: float
    :param minValue: clamp/stop any value below this value
    :type minValue: float
    :param maxValue: clamp/stop any value above this value
    :type maxValue: float
    :return clampedValue: clamped value as a float
    :rtype clampedValue: float
    """
    return max(minValue, min(value, maxValue))


def groupNumericByRanges(ranges, values):
    """Given a list of ranges and values return a list of values within each range.

    ..code-block:

        groupNumericByRanges([[0, 0.75], [0.75, 1.0]], [0.0,0.25,0.5.0,0.75,1.0])
        # result: [[0.0,0.25,0.50, 0.75],[0.75, 1.0]]


    :param ranges:
    :type ranges: list[list[float]]
    :param values:
    :type values: list[float]
    :return: Generator which returns a list of floats for each range.
    :rtype: list[float]
    """
    for minValue, maxValue in ranges:
        yield [
            param for param in values if minValue <= param <= maxValue
        ]


if sys.version_info[0] >= 3:
    round = round
else:
    def round(value, ndigits=0):
        """Helper function to make py2 and py3 compatible rounding so that py2 acts like py3.
        The return value is an integer if ndigits is omitted or None.  Otherwise
        the return value has the same type as the number.  ndigits may be negative.
        :param value:
        :type value:
        :param ndigits:
        :type ndigits:
        :return:
        :rtype:

        """
        context = decimal.getcontext()
        context.rounding = decimal.ROUND_HALF_EVEN
        d = decimal.Decimal(str(value))
        return float(d.quantize(decimal.Decimal('1e-%d' % ndigits)))


# Linear tangent type. Tangent is zero-length, the curve passes through the point directly.
kLinear = 0
# Spline tangent type. Tangent direction is defined by `inDir` or `outDir` and weighted by tangent length.
kSpline = 1
# Smooth tangent type. Tangent is automatically computed to create a smooth curve between neighboring points.
kSmooth = 2

class BezierCurve(object):
    """Represents a multi-point cubic Bezier curve with support for different tangent types.

    Each point can have incoming and outgoing tangents of type:
    - kLinear: tangent is zero-length (anchor only)
    - kSpline: tangent follows a specified direction vector
    - kSmooth: tangent automatically computed to create a smooth curve

    :param points: List of Point objects defining the curve (must contain at least 2 points)
    :type points: list[BezierCurve.Point]

    ..code-block:: python

        points = [
            BezierCurve.Point(0, 0, outType=kLinear, outWeight=6.0),
            BezierCurve.Point(10, 0.3, inType=kSmooth, outType=kSmooth,
                              inWeight=6.0, outWeight=6.0),
            BezierCurve.Point(20, 0, inType=kSmooth, inWeight=10.0)
        ]
        curve = BezierCurve(points)
        curve.printAscii(0, 20, width=60, height=20)
        y_val = curve.evaluate(10)  # Get y value at x = 10

    """
    class Point:
        """Represents a single anchor point in a Bezier curve, including tangent types and weights.

        :param x: X-coordinate of the point (time or horizontal axis)
        :type x: float
        :param y: Y-coordinate of the point (value or vertical axis)
        :type y: float
        :param inType: Type of the incoming tangent (kLinear, kSpline, kSmooth)
        :type inType: int
        :param outType: Type of the outgoing tangent (kLinear, kSpline, kSmooth)
        :type outType: int
        :param inWeight: Weight/length of the incoming tangent
        :type inWeight: float
        :param outWeight: Weight/length of the outgoing tangent
        :type outWeight: float
        :param inDir: Direction vector for the incoming tangent (used for spline)
        :type inDir: tuple(float, float)
        :param outDir: Direction vector for the outgoing tangent (used for spline)
        :type outDir: tuple(float, float)
        """
        def __init__(self, x, y, inType=kSpline, outType=kSpline,
                     inWeight=1.0, outWeight=1.0,
                     inDir=(0, 0), outDir=(0, 0)):
            self.x = x
            self.y = y
            self.inType = inType
            self.outType = outType
            self.inWeight = inWeight
            self.outWeight = outWeight
            self.inDir = inDir
            self.outDir = outDir
            self.inTangent = (x, y)
            self.outTangent = (x, y)

    def __init__(self, points):
        super(BezierCurve, self).__init__()
        if len(points) < 2:
            raise ValueError("Bezier curve needs at least 2 points")
        self.points = points
        self._computeTangents()

    def evaluate(self, t):
        """Evaluate the Bezier curve and return the y value for a given x=t.

        :param t: X-coordinate to evaluate the curve
        :type t: float
        :return: Y-coordinate of the curve at x=t, or None if t is out of range
        :rtype: float or None
        """
        for i in range(len(self.points) - 1):
            p0, p1 = self.points[i], self.points[i + 1]
            if p0.x <= t <= p1.x:
                u = self._findUForX(p0, p1, t)
                _, y = self._evalSegment(p0, p1, u)
                return y
        return None

    def printAscii(self, xMin, xMax, width=60, height=20, samples=500):
        """Print an ASCII art representation of the Bezier curve.

        :param xMin: Minimum X value to display
        :type xMin: float
        :param xMax: Maximum X value to display
        :type xMax: float
        :param width: Width of the ASCII grid
        :type width: int
        :param height: Height of the ASCII grid
        :type height: int
        :param samples: Number of sample points to evaluate along the curve
        :type samples: int
        """
        xs = [xMin + i * (xMax - xMin) / (samples - 1) for i in range(samples)]
        ys = [self.evaluate(x) for x in xs if self.evaluate(x) is not None]

        if not ys:
            print("Curve has no values in range.")
            return

        ymin, ymax = min(ys), max(ys)
        for p in self.points:
            ymin = min(ymin, p.inTangent[1], p.outTangent[1])
            ymax = max(ymax, p.inTangent[1], p.outTangent[1])

        if ymin == ymax:
            ymin -= 1
            ymax += 1

        scaleX = (xMax - xMin) / (width - 1)
        scaleY = (ymax - ymin) / (height - 1)

        grid = [[" " for _ in range(width)] for _ in range(height)]

        # Plot curve
        for x in xs:
            y = self.evaluate(x)
            if y is None:
                continue
            col = int((x - xMin) / scaleX)
            row = int((ymax - y) / scaleY)
            if 0 <= row < height and 0 <= col < width:
                grid[row][col] = "*"

        # Plot tangent points
        for p in self.points:
            for tx, ty in [p.inTangent, p.outTangent]:
                col = int((tx - xMin) / scaleX)
                row = int((ymax - ty) / scaleY)
                if 0 <= row < height and 0 <= col < width:
                    grid[row][col] = "+"

        for row in grid:
            print("".join(row))

    def _normalize(self, dx, dy):
        """Normalize a 2D vector.

        :param dx: X component
        :type dx: float
        :param dy: Y component
        :type dy: float
        :return: Normalized vector (nx, ny)
        :rtype: tuple(float, float)
        """
        length = (dx * dx + dy * dy) ** 0.5
        if length == 0:
            return 0, 0
        return dx / length, dy / length

    def _computeTangents(self):
        """Compute in/out tangents for all points based on their type and weight.
        """
        n = len(self.points)
        for i, p in enumerate(self.points):
            # Out tangent
            if p.outType == kLinear:
                p.outTangent = (p.x, p.y)
            elif p.outType == kSmooth and 0 < i < n - 1:
                dx = self.points[i + 1].x - self.points[i - 1].x
                dy = self.points[i + 1].y - self.points[i - 1].y
                nx, ny = self._normalize(dx, dy)
                p.outTangent = (p.x + nx * p.outWeight, p.y + ny * p.outWeight)
            elif p.outType == kSpline:
                nx, ny = self._normalize(*p.outDir)
                p.outTangent = (p.x + nx * p.outWeight, p.y + ny * p.outWeight)
            else:
                p.outTangent = (p.x, p.y)

            # In tangent
            if p.inType == kLinear:
                p.inTangent = (p.x, p.y)
            elif p.inType == kSmooth and 0 < i < n - 1:
                dx = self.points[i - 1].x - self.points[i + 1].x
                dy = self.points[i - 1].y - self.points[i + 1].y
                nx, ny = self._normalize(dx, dy)
                p.inTangent = (p.x + nx * p.inWeight, p.y + ny * p.inWeight)
            elif p.inType == kSpline:
                nx, ny = self._normalize(*p.inDir)
                p.inTangent = (p.x + nx * p.inWeight, p.y + ny * p.inWeight)
            else:
                p.inTangent = (p.x, p.y)

    def _evalSegment(self, p0, p1, u):
        """Evaluate cubic Bezier segment between two points.

        :param p0: Start point of segment
        :type p0: BezierCurve.Point
        :param p1: End point of segment
        :type p1: BezierCurve.Point
        :param u: Parametric value in [0,1]
        :type u: float
        :return: (x, y) coordinates on the segment
        :rtype: tuple(float, float)
        """
        x0, y0 = p0.x, p0.y
        x3, y3 = p1.x, p1.y
        x1, y1 = p0.outTangent
        x2, y2 = p1.inTangent

        x = ((1 - u) ** 3) * x0 + 3 * ((1 - u) ** 2) * u * x1 + 3 * (1 - u) * (u ** 2) * x2 + (u ** 3) * x3
        y = ((1 - u) ** 3) * y0 + 3 * ((1 - u) ** 2) * u * y1 + 3 * (1 - u) * (u ** 2) * y2 + (u ** 3) * y3
        return x, y

    def _findUForX(self, p0, p1, t, maxIter=20, tol=1e-5):
        """Solve x(u) = t for a Bezier segment using binary search.

        :param p0: Start point of segment
        :type p0: BezierCurve.Point
        :param p1: End point of segment
        :type p1: BezierCurve.Point
        :param t: Target x value
        :type t: float
        :param maxIter: Maximum number of iterations
        :type maxIter: int
        :param tol: Tolerance for convergence
        :type tol: float
        :return: Parametric value u in [0,1] where x(u) ≈ t
        :rtype: float
        """
        """Solve x(u) = t using binary search."""
        u0, u1 = 0.0, 1.0
        for _ in range(maxIter):
            umid = (u0 + u1) / 2
            xmid, _ = self._evalSegment(p0, p1, umid)
            if abs(xmid - t) < tol:
                return umid
            if xmid < t:
                u0 = umid
            else:
                u1 = umid
        return (u0 + u1) / 2
