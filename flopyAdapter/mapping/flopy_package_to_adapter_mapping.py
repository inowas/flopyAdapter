"""
Mapping of flopy package names to modflow adapters

"""

from flopyAdapter.modflow_package_adapter.basadapter import BasAdapter
from flopyAdapter.modflow_package_adapter.chdadapter import ChdAdapter
from flopyAdapter.modflow_package_adapter.disadapter import DisAdapter
from flopyAdapter.modflow_package_adapter.drnadapter import DrnAdapter
from flopyAdapter.modflow_package_adapter.ghbadapter import GhbAdapter
from flopyAdapter.modflow_package_adapter.hobadapter import HobAdapter
from flopyAdapter.modflow_package_adapter.lpfadapter import LpfAdapter
from flopyAdapter.modflow_package_adapter.mfadapter import MfAdapter
from flopyAdapter.modflow_package_adapter.nwtadapter import NwtAdapter
from flopyAdapter.modflow_package_adapter.ocadapter import OcAdapter
from flopyAdapter.modflow_package_adapter.pcgadapter import PcgAdapter
from flopyAdapter.modflow_package_adapter.rchadapter import RchAdapter
from flopyAdapter.modflow_package_adapter.evtadapter import EvtAdapter
from flopyAdapter.modflow_package_adapter.rivadapter import RivAdapter
from flopyAdapter.modflow_package_adapter.upwadapter import UpwAdapter
from flopyAdapter.modflow_package_adapter.weladapter import WelAdapter
from flopyAdapter.modflow_package_adapter.lmtadapter import LmtAdapter
from flopyAdapter.modflow_package_adapter.mpadapter import MpAdapter
from flopyAdapter.modflow_package_adapter.mpbasadapter import MpBasAdapter
from flopyAdapter.modflow_package_adapter.mpsimadapter import MpSimAdapter
from flopyAdapter.modflow_package_adapter.mtadapter import MtAdapter
from flopyAdapter.modflow_package_adapter.advadapter import AdvAdapter
from flopyAdapter.modflow_package_adapter.btnadapter import BtnAdapter
from flopyAdapter.modflow_package_adapter.dspadapter import DspAdapter
from flopyAdapter.modflow_package_adapter.gcgadapter import GcgAdapter
from flopyAdapter.modflow_package_adapter.lktadapter import LktAdapter
from flopyAdapter.modflow_package_adapter.phcadapter import PhcAdapter
from flopyAdapter.modflow_package_adapter.rctadapter import RctAdapter
from flopyAdapter.modflow_package_adapter.sftadapter import SftAdapter
from flopyAdapter.modflow_package_adapter.ssmadapter import SsmAdapter
from flopyAdapter.modflow_package_adapter.tobadapter import TobAdapter
from flopyAdapter.modflow_package_adapter.uztadapter import UztAdapter
from flopyAdapter.modflow_package_adapter.swtadapter import SwtAdapter
from flopyAdapter.modflow_package_adapter.vdfadapter import VdfAdapter
from flopyAdapter.modflow_package_adapter.vscadapter import VscAdapter

FLOPY_PACKAGE_TO_ADAPTER_MAPPER = {
    # Main adapters
    "mf": MfAdapter,
    "mt": MtAdapter,
    "mp": MpAdapter,
    "mpbas": MpBasAdapter,
    "mpsim": MpSimAdapter,
    # Package adapters
    "adv": AdvAdapter,
    "bas": BasAdapter,
    "bas6": BasAdapter,
    "btn": BtnAdapter,
    "chd": ChdAdapter,
    "dis": DisAdapter,
    "drn": DrnAdapter,
    "dsp": DspAdapter,
    "evt": EvtAdapter,
    "gcg": GcgAdapter,
    "ghb": GhbAdapter,
    "hob": HobAdapter,
    "lkt": LktAdapter,
    "lmt": LmtAdapter,
    "lpf": LpfAdapter,
    "nwt": NwtAdapter,
    "oc": OcAdapter,
    "pcg": PcgAdapter,
    "phc": PhcAdapter,
    "rch": RchAdapter,
    "rct": RctAdapter,
    "riv": RivAdapter,
    "sft": SftAdapter,
    "ssm": SsmAdapter,
    "swt": SwtAdapter,
    "tob": TobAdapter,
    "upw": UpwAdapter,
    "uzt": UztAdapter,
    "vdf": VdfAdapter,
    "vsc": VscAdapter,
    "wel": WelAdapter
}
