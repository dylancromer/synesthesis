import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['figure.dpi'] = 150
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'figure.autolayout': True})
import seaborn as sns
sns.set(
    style='whitegrid',
    font_scale=0.9,
    rc={'lines.linewidth': 1.4, 'lines.markersize': 1.6},
)
from jupyterthemes import jtplot
jtplot.style(theme='oceans16')
jtplot.style(context='notebook', fscale=1, spines=False, gridlines='--')
BGD = '#1b1e28'
style_dict = {
    'figure.edgecolor': BGD,
    'figure.facecolor': BGD,
    'axes.facecolor': BGD,
    'axes.edgecolor': BGD,
    'grid.color': BGD,
    'patch.edgecolor': BGD,
    'patch.facecolor': BGD,
    'savefig.facecolor': BGD,
    'savefig.edgecolor': BGD,
}
matplotlib.rcParams.update(style_dict)
from mpl_toolkits import mplot3d
from mpl_toolkits import mplot3d
from matplotlib import animation
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Source Code Pro']
from matplotlib.patches import FancyArrowPatch


class Arrow3D(FancyArrowPatch):
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._xyz = (x,y,z)
        self._dxdydz = (dx,dy,dz)

    def draw(self, renderer):
        x1,y1,z1 = self._xyz
        dx,dy,dz = self._dxdydz
        x2,y2,z2 = (x1+dx,y1+dy,z1+dz)

        xs, ys, zs = mplot3d.proj3d.proj_transform((x1,x2),(y1,y2),(z1,z2), renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        super().draw(renderer)


def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


setattr(mplot3d.Axes3D, 'arrow3D', _arrow3D)


color_vals = (33//1.2, 36//1.2, 48//1.2)
PLOT_BACKGROUND_COLOR = (color_vals[0]/255, color_vals[1]/255, color_vals[2]/255, 1)
COLOR = '#46a5ce'
ALPHA = 0.4
ELEV = None
AZIM = 45
NUM_WIRES = 100
FRAMERATE = 60
VIDEO_DPI = 300
DELAY_SECONDS = 3
DELAY_FRAMES = int(DELAY_SECONDS*60)
FRAMES_PER_DEGREE = 2
NUM_FRAMES = FRAMES_PER_DEGREE*360 + DELAY_FRAMES #one frame per 1/FRAMES_PER_DEGREE degree rotation


def animate_spectrum(times, freqs, spectrum, outfile):
    fig = plt.figure()
    X, Y = np.meshgrid(freqs, times)
    ax = mplot3d.Axes3D(fig)

    def init():
        ax.plot_wireframe(
            X,
            Y,
            spectrum,
            color=COLOR,
            alpha=ALPHA,
            rcount=NUM_WIRES,
            ccount=NUM_WIRES,
        )
        ax.w_xaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
        ax.w_yaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
        ax.w_zaxis.set_pane_color(PLOT_BACKGROUND_COLOR)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.view_init(elev=ELEV, azim=AZIM)

        xtail = (0.2*freqs.max(), 1.1*times.max(), 0*spectrum.max())
        xdelta = (0.6*freqs.max(), 0*times.max(), 0*spectrum.max())
        ax.arrow3D(*xtail, *xdelta, fc='#afbfd1', mutation_scale=12)
        ax.set_xlabel('frequency', labelpad=0)

        ytail = (1.1*freqs.max(), 0.2*times.max(), 0*spectrum.max())
        ydelta = (0*freqs.max(), 0.6*times.max(), 0*spectrum.max())
        ax.arrow3D(*ytail, *ydelta, fc='#afbfd1', mutation_scale=12)
        ax.set_ylabel(' time ', labelpad=0)

        ztail = (1.1*freqs.max(), 0*times.max(), 0.2*spectrum.max())
        zdelta = (0*freqs.max(), 0*times.max(), 0.6*spectrum.max())
        ax.arrow3D(*ztail, *zdelta, fc='#afbfd1', mutation_scale=16)
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel('power', rotation=90, labelpad=0)

        ax.grid(None)
        return fig,

    def animate(i):
        if i < DELAY_FRAMES:
            return fig,
        else:
            j = i - DELAY_FRAMES
            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_zlabel('')
            ax.view_init(elev=ELEV, azim=AZIM+j/FRAMES_PER_DEGREE)
            return fig,

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=NUM_FRAMES, interval=20, blit=True)

    anim.save(outfile, dpi=VIDEO_DPI, fps=FRAMERATE, bitrate=-1, extra_args=['-vcodec', 'libx264'])
