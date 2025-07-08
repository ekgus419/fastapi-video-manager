from src.domain.video_view_log_domain import VideoViewLogDomain
from src.entity import VideoViewLogEntity


def entity_to_domain(entity: VideoViewLogEntity) -> VideoViewLogDomain:
    """
    엔티티(Entity) → 도메인(Domain) 변환 함수
    - DB에서 조회한 ORM 엔티티 객체를 비즈니스 로직 계층에서 사용할 도메인 객체로 변환합니다.
    - Service 계층은 도메인만을 다루도록 구성하기 위해 사용됩니다.
    """
    return VideoViewLogDomain(
        id=entity.id,
        user_id=entity.user_id,
        video_id=entity.video_id,
        viewed_at=entity.viewed_at,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        deleted_at=entity.deleted_at
    )


def domain_to_entity(domain: VideoViewLogDomain) -> VideoViewLogEntity:
    """
    도메인(Domain) → 엔티티(Entity) 변환 함수
    - 비즈니스 계층에서 생성/수정한 도메인 객체를 DB에 저장할 수 있도록 ORM 엔티티로 변환합니다.
    - Repository 계층에 전달할 때 사용됩니다.
    """
    return VideoViewLogEntity(
        user_id=domain.user_id,
        video_id=domain.video_id,
        viewed_at=domain.viewed_at,
    )
