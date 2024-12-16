from ophyd import EpicsMotor, PseudoPositioner, PseudoSingle, Component as Cpt
from ophyd.pseudopos import pseudo_position_argument, real_position_argument
from nbs_bl.printing import boxed_text
from .motors import FMBOEpicsMotor


class QuadSlitsBase(PseudoPositioner):
    """
    Base class for quad slits.

    Parameters
    ----------
    *args
        Arguments to pass to parent class
    **kwargs
        Keyword arguments to pass to parent class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def where(self):
        print("%s:" % self.name)
        text1 = "      vertical   size   = %7.3f mm\n" % (self.vsize.position)
        text1 += "      vertical   center = %7.3f mm\n" % (self.vcenter.position)
        text2 = "      horizontal size   = %7.3f mm\n" % (self.hsize.position)
        text2 += "      horizontal center = %7.3f mm\n" % (self.hcenter.position)
        return text1 + text2

    def wh(self):
        boxed_text(self.name, self.where(), "cyan")

    # The pseudo positioner axes:
    vsize = Cpt(PseudoSingle, limits=(-1, 20), kind="hinted")
    vcenter = Cpt(PseudoSingle, limits=(-10, 10), kind="normal")
    hsize = Cpt(PseudoSingle, limits=(-1, 20), kind="hinted")
    hcenter = Cpt(PseudoSingle, limits=(-10, 10), kind="normal")

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        """
        Run a forward (pseudo -> real) calculation.

        Parameters
        ----------
        pseudo_pos : PseudoPosition
            The pseudo position to calculate real positions for

        Returns
        -------
        RealPosition
            The real motor positions
        """
        return self.RealPosition(
            top=pseudo_pos.vcenter + pseudo_pos.vsize / 2,
            bottom=pseudo_pos.vcenter - pseudo_pos.vsize / 2,
            outboard=pseudo_pos.hcenter + pseudo_pos.hsize / 2,
            inboard=pseudo_pos.hcenter - pseudo_pos.hsize / 2,
        )

    @real_position_argument
    def inverse(self, real_pos):
        """
        Run an inverse (real -> pseudo) calculation.

        Parameters
        ----------
        real_pos : RealPosition
            The real positions to calculate pseudo positions for

        Returns
        -------
        PseudoPosition
            The pseudo axis positions
        """
        return self.PseudoPosition(
            hsize=real_pos.outboard - real_pos.inboard,
            hcenter=(real_pos.outboard + real_pos.inboard) / 2,
            vsize=real_pos.top - real_pos.bottom,
            vcenter=(real_pos.top + real_pos.bottom) / 2,
        )


class QuadSlits(QuadSlitsBase):
    """
    Quad slits implementation using standard EpicsMotors.
    """

    # The real (or physical) positioners:
    top = Cpt(EpicsMotor, "T}Mtr", kind="normal")
    bottom = Cpt(EpicsMotor, "B}Mtr", kind="normal")
    inboard = Cpt(EpicsMotor, "I}Mtr", kind="normal")
    outboard = Cpt(EpicsMotor, "O}Mtr", kind="normal")


class FMBOQuadSlits(QuadSlitsBase):
    """
    Quad slits implementation using FMBOEpicsMotors.
    """

    # The real (or physical) positioners:
    top = Cpt(FMBOEpicsMotor, "T}Mtr", kind="normal")
    bottom = Cpt(FMBOEpicsMotor, "B}Mtr", kind="normal")
    inboard = Cpt(FMBOEpicsMotor, "I}Mtr", kind="normal")
    outboard = Cpt(FMBOEpicsMotor, "O}Mtr", kind="normal")
