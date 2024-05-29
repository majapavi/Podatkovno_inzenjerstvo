import abc  #omogucuje definiranje apstraktnih klasa i metoda   

class IDetectionAPI(abc.ABC):

    @abc.abstractmethod
    def detect_files(self):
        raise NotImplementedError("method must be implemented")

