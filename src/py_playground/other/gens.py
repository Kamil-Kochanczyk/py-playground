import logging
from collections.abc import Iterator


def countdown(n: int) -> Iterator[int]:
    if n < 1:
        raise ValueError("n must be no smaller than 1")
    while n >= 1:
        yield n
        n -= 1


def echo_gen(logger: logging.Logger) -> Iterator[None]:
    try:
        while True:
            received = yield
            logger.info(received)
    finally:
        logger.info("Echo generator closed!")


def main() -> None:
    logging.basicConfig(format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%H:%M:%S")
    logger = logging.getLogger("Gens")
    logger.setLevel(logging.INFO)

    generator1 = countdown(10)  # returns an iterator

    logger.info(generator1)

    # generator returns values on the fly and saves memory
    for i in generator1:
        logger.info(i)

    generator2 = (x * x for x in range(1, 11) if x % 2 == 0)

    logger.info(generator2)

    for i in generator2:
        logger.info(i)

    generator3 = (list(word.encode("utf-8")) for word in ["bello", "papaja"])

    try:
        while True:
            logger.info(next(generator3))
    except StopIteration:
        logger.exception("Generator yielded all values!")

    # generators are for one-time use only - once the genarator is exhausted, it cannot be used again
    # for i in generator1:
    #     logger.info(i)
    # logger.info(sum(generator1))

    generator5 = countdown(5)
    logger.info(sum(generator5))
    for i in generator5:
        logger.info(i)

    # send() passes values to the generator, close() closes the generator
    echo = echo_gen(logger)
    next(echo)
    echo.send("Bello")  # type: ignore[]
    echo.send("papaja")  # type: ignore[]
    echo.send("!")  # type: ignore[]
    echo.close()  # type: ignore[]
    # echo.send("Hi")


if __name__ == "__main__":
    main()
